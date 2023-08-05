# -*- coding: utf8 -*-
#
#    Copyright (C) 2021 NDP Systèmes (<http://www.ndp-systemes.fr>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# pylint: disable=W0703

import logging
import os
import sys
from io import BytesIO

from minio import Minio

if sys.version_info[0] == 3:
    from minio.deleteobjects import DeleteObject
    from minio.error import S3Error
else:
    from minio.error import MinioError as S3Error

    def DeleteObject(*args):  # noqa
        return args


from typing import Dict, Iterable, List, Optional, Tuple, Union

_logger = logging.getLogger(__name__)


class S3ConnectInfo(object):
    def __init__(self, host, access_key, secret, region="us-east-1"):
        # type: (str, str, str, Optional[str]) -> S3ConnectInfo
        self._access_key = access_key
        self._secret = secret
        self._region = region or "us-east-1"
        self._host = host

    @property
    def access_key(self):
        # type: () -> str
        return self._access_key

    @property
    def secret(self):
        # type: () -> str
        return self._secret

    @property
    def region(self):
        # type: () -> str
        return self._region

    @property
    def host(self):
        # type: () -> str
        return self._host

    @property
    def enable(self):
        # type: () -> bool
        return bool(self.host and self.secret and self.access_key and self.region)

    @property
    def s3_session(self):
        # type: () -> Minio
        return Minio(
            self.host,
            access_key=self.access_key,
            secret_key=self.secret,
            region=self.region,
        )


class S3OdooBucketInfo(object):
    def __init__(self, name, sub_dir_name=None, checklist_dir=None):
        # type: (str, Optional[str], Optional[str]) -> S3OdooBucketInfo
        """
        Represente la configurtation d'un bucket S3
        :param name: LE nom du bucket : obligatoire
        :param sub_dir_name: Non d'un dossier inclut lors de la création d'une clef
        :param checklist_dir: Nom du dossier pour faire la gestion des fichiers à supprimer
        """
        assert name
        self.name = name
        self.sub_dir_name = sub_dir_name
        self.checklist_dir = checklist_dir or "checklist"

    def get_key(self, *file_paths):
        # type: (List[str]) -> str
        """
        Retourne la clef pour la paire db_name et file_name

        Si la connexion (self.conn) à été créée avec **sub_dir_by_db** à Vrai alors le format sera <db_name>/<file_name>
        Sinon uniquement file_names sera retourné séparé par des '/'
        :param file_paths: un tableau de 1 ou n constituant le chemain sous first-dir
        du fichier dans le bucket, supprime les valeur <False>
        :return: self.sub_dir_name/*file_paths ir sub_dir_name is provided
        """
        keys = [f for f in file_paths if f]
        if bool(self.sub_dir_name):
            keys.insert(0, self.sub_dir_name)
        return "/".join(keys)


def get_from_env(*keys):
    for key in keys:
        r = os.environ.get(key)
        if r:
            return r
    return None


class S3Odoo(object):
    def __init__(self, connection, bucket):
        # type: (S3ConnectInfo, S3OdooBucketInfo) -> None
        self.conn = connection
        self.bucket = bucket

    @staticmethod
    def get_connection(host, access_key, secret, region, bucket_name, db_name=None):
        # type: (str, str, str, str,str, Optional[str]) -> S3Odoo
        """
        Créer une instance de S3Odoo avec les parametres fournit.
        `db_name` permet d'avoir un dossier ou tous les enregistrements
         fait par file_write seront automatiquement dedans
         Voir aussi S3ConnectInfo#__init__, S3OdooBucketInfo#__init__
        :param host: le host du serveur S3 fournit par votre fournisseur S3
        :param access_key: la clef d'acces fournit par votre fournisseur S3
        :param secret: le secret d'acces fournit par votre fournisseur S3
        :param region: la region ou se trouve votre S3 fournit par votre fournisseur S3
        :param bucket_name: le nom du bucket à utiliser
        :param db_name: le nom du repertoire principal à utiliser dans le bucket
        :return:
        """
        return S3Odoo(
            S3ConnectInfo(host=host, access_key=access_key, secret=secret, region=region),
            S3OdooBucketInfo(name=bucket_name, sub_dir_name=db_name),
        )

    @staticmethod
    def from_env(db_name=None):
        # type: (Optional[str]) -> S3Odoo
        use_main_dir = bool(os.environ.get("S3_FILESTORE_SUB_DIR"))
        if use_main_dir and not db_name:
            raise ValueError("db_name not provided but your environ variable to required it are set")
        dbname = db_name if use_main_dir else None
        access_key = get_from_env("S3_FILESTORE_ACCESS_KEY", "CELLAR_ADDON_KEY_ID", "ODOO_S3_ACCESS_KEY")
        secret = get_from_env("S3_FILESTORE_SECRET_KEY", "CELLAR_ADDON_KEY_SECRET", "ODOO_S3_SECRET_KEY")
        region = get_from_env("S3_FILESTORE_REGION", "ODOO_S3_REGION") or "fr-par"
        host = get_from_env("S3_FILESTORE_HOST", "CELLAR_ADDON_HOST", "ODOO_S3_HOST")
        bucket_name = get_from_env("S3_FILESTORE_BUCKET", "ODOO_S3_BUCKET")
        return S3Odoo.get_connection(
            host=host, access_key=access_key, secret=secret, region=region, bucket_name=bucket_name, db_name=dbname
        )

    def get_key(self, *file_paths):
        # type: (List[str]) -> str
        """
        Voir S3OdooBucketInfo#get_key
        :param file_paths: le path du fichier dans une liste
        :return: le path du fichier
        """
        return self.bucket.get_key(*file_paths)

    def bucket_exist(self):
        # type: () -> bool
        """
        Retourn vrai si le bucket fournit lors de l'instanciation
        :return: Vrai si le bucket existe
        """
        return self.conn.s3_session.bucket_exists(self.bucket.name)

    def delete_bucket(self):
        # type: () -> bool
        """
        Supprime le bucket founit au debut de l'instanciation
        :return: Vrai si la suppression à reussi
        """
        try:
            s3_session = self.conn.s3_session
        except Exception as e:
            _logger.error("S3: create_bucket_if_not_exist Was not able to connect to S3 (%s)", exc_info=e)
            return False
        try:
            s3_session.remove_bucket(self.bucket.name)
            return True
        except S3Error as e:
            _logger.error(
                "S3: create_bucket_if_not_exist Was not able to create bucket %s to S3 (%s)",
                self.bucket.name,
                exc_info=e,
            )
        return False

    def create_bucket_if_not_exist(self):
        # type: () -> bool
        """
        Retourne Vrai **si et uniquement si** le bucket à été créé
        Faut si le bucket existait deja ou si il ya eu une erreur
        :return: Vrai si la création à reussi
        """
        try:
            s3_session = self.conn.s3_session
        except Exception as e:
            _logger.error("S3: create_bucket_if_not_exist Was not able to connect to S3 (%s)", exc_info=e)
            return False
        try:
            if not self.bucket_exist():
                s3_session.make_bucket(self.bucket.name)
                _logger.info("S3: bucket [%s] created successfully", self.bucket.name)
                return True
        except S3Error as e:
            _logger.error(
                "S3: create_bucket_if_not_exist Was not able to create bucket %s to S3 (%s)",
                self.bucket.name,
                exc_info=e,
            )
            return False
        return False

    def file_exist(self, fname, first_dir=None):
        # type: (str, Optional[str]) -> bin
        """
        Test l'existance du de l'objet avec le nom `fname`
        :param fname: non de l'object dont il faut tester l'existence
        :param first_dir: un dossier parent au fname si besoin
        :return: Vrai si l'object avec le fname existe
        """
        try:
            s3_session = self.conn.s3_session
        except Exception as e:
            _logger.error("S3: _file_read Was not able to connect to S3 (%s)", exc_info=e)
            return b""

        key = self.bucket.get_key(first_dir, fname)
        res = False
        s3_key = None
        try:
            bucket_name = self.bucket.name
            s3_key = s3_session.get_object(bucket_name, key)
            res = True
        except S3Error as e:
            _logger.debug("S3: S3Error _file_read was not able to read from S3 (%s): %s", key, exc_info=e)
            res = False
        except Exception as e:
            _logger.error("S3: _file_read was not able to read from S3 (%s): %s", key, exc_info=e)
            raise e
        finally:
            if s3_key:
                s3_key.close()
                s3_key.release_conn()
        return res

    def file_read(self, fname, first_dir=None):
        # type: (str, Optional[str]) -> bin
        """
        Lit l'objet avec le nom `fname`
        `first_dir` sert si besoin à preciser un dossier parent
        :param fname: le nom du fichier, peut contenir une arborecence
        :param first_dir: le nom d'un dossier parent
        :return: une valeur binaire
        """
        try:
            s3_session = self.conn.s3_session
        except Exception as e:
            _logger.error("S3: _file_read Was not able to connect to S3 (%s)", e)
            return b""

        s3_key = None
        bucket_name = self.bucket.name
        key = self.bucket.get_key(first_dir, fname)
        try:
            s3_key = s3_session.get_object(bucket_name, key)
            res = s3_key.data
            _logger.debug("S3: _file_read read %s:%s from bucket successfully", bucket_name, key)
        except S3Error as e:
            _logger.debug("S3: S3Error _file_read was not able to read from S3 (%s): %s", key, exc_info=e)
            return b""
        except Exception as e:
            _logger.error("S3: _file_read was not able to read from S3 (%s): %s", key, exc_info=e)
            raise e
        finally:
            if s3_key:
                s3_key.close()
                s3_key.release_conn()
        return res

    def file_write(self, fname, value, first_dir=None):
        # type: (str, bin, str) -> str
        """
        Ecrit la valeur (`value`) dans le S3 sous le nom `fname`
        `first_dir` permet de préciser un sous dossier si necessaire
        :param fname: nom du fichier, peut contenir l'arboressence complete (Ex: my-dir/file.txt)
        :param value: la valeur binaire
        :param first_dir: un dossier parent au fname
        :return: fname
        """
        try:
            s3_session = self.conn.s3_session
        except S3Error as e:
            _logger.error("S3: _file_write was not able to connect (%s)", e)
            return fname

        bucket_name = self.bucket.name
        key = self.get_key(first_dir, fname)
        try:
            s3_session.put_object(bucket_name, key, BytesIO(value), len(value))
            _logger.debug("S3: _file_write %s:%s was successfully uploaded", bucket_name, key)
        except S3Error as e:
            _logger.error("S3: _file_write was not able to write (%s): %s", key, e)
            raise e
        # Returning the file name
        return fname

    def mark_for_gc(self, fname):
        # type: (str) -> Union[str, None]
        """
        Met un fichier vide (valeur de 0bytes) dans un sous dossier "checklist" avec le nom fournit en paramettre
        :param fname: le nom du fichier
        :return: fname
        """
        return self.file_write(fname, b"", "checklist")

    def file_delete(self, fname):
        # type: (str) -> bool
        """
        Supprime le fichier ayant le `fname` et retourne Vrai si il n'y a pas d'erreur
        :param fname: le nom du fichier à supprimer
        :return: Vrai si la suppression ne leve pa d'erreur
        """
        try:
            s3_session = self.conn.s3_session
        except Exception as e:
            _logger.error("S3: file_delete was not able to connect (%s)", e)
            return False
        bucket_name = self.bucket.name
        key = self.bucket.get_key(fname)
        try:
            s3_session.stat_object(bucket_name, key)
            try:
                s3_session.remove_object(bucket_name, key)
                _logger.debug("S3: _file_delete deleted %s:%s successfully", bucket_name, key)
            except Exception as e:
                _logger.error("S3: _file_delete was not able to gc (%s:%s) : %s", bucket_name, key, e)
                return False
        except Exception as e:
            _logger.error("S3: _file_delete get_stat was not able to gc (%s:%s) : %s", bucket_name, key, e)
            return False
        return True

    def get_checklist_objects(self):
        # type: () -> Dict[str, Tuple[str, str]]
        checklist = {}
        prefix = self.get_key("checklist")
        # retrieve the file names from the checklist
        for s3_key_gc in self.conn.s3_session.list_objects(self.bucket.name, prefix=prefix, recursive=True):
            if not s3_key_gc.is_dir:
                fname = s3_key_gc.object_name[len(prefix + "/") :]
                real_key_name = fname
                if self.bucket.sub_dir_name:
                    real_key_name = "%s/%s" % (self.bucket.sub_dir_name, fname)
                checklist[fname] = (real_key_name, s3_key_gc.object_name)
        return checklist

    def file_delete_multi(self, to_deletes, whitelist=None):
        # type: (Dict[str, str], Iterable[str]) -> int
        whitelist = whitelist or []
        removed = 0
        to_mass_deletes = []

        for real_key_name, check_key_name in to_deletes.values():
            to_mass_deletes.append(DeleteObject(check_key_name))
            if not whitelist or real_key_name not in whitelist:
                to_mass_deletes.append(DeleteObject(self.get_key(real_key_name)))

        try:
            errors = list(self.conn.s3_session.remove_objects(self.bucket.name, to_mass_deletes))
            removed = len(to_mass_deletes) and len(to_mass_deletes) - len(errors) or 0
            _logger.debug("S3: _file_gc_s3 deleted %s:%s successfully", self.bucket.name, removed)
        except Exception as e:
            _logger.error("S3: _file_gc_s3 was not able to gc (%s) : %s", self.bucket.name, e)
        return removed
