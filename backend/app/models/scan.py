from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
from typing import Dict, Any, Optional, List
from config import Config

client = MongoClient(Config.MONGODB_URI)
db = client.get_default_database()

class Scan:
    def __init__(self, target: str, scan_type: str, user_id: Optional[str] = None,
                 status: str = "pending", results: Optional[Dict] = None, _id: Optional[str] = None):
        self._id = _id
        self.target = target
        self.scan_type = scan_type
        self.user_id = user_id
        self.status = status  # pending, running, completed, error
        self.results = results or {}
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self) -> str:
        """Sauvegarde le scan dans la base de données"""
        scan_data = {
            'target': self.target,
            'scan_type': self.scan_type,
            'user_id': self.user_id,
            'status': self.status,
            'results': self.results,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

        if self._id:  # Update
            db.scans.update_one(
                {'_id': ObjectId(self._id)},
                {'$set': {
                    **scan_data,
                    'updated_at': datetime.utcnow()
                }}
            )
            return self._id
        else:  # Insert
            result = db.scans.insert_one(scan_data)
            self._id = str(result.inserted_id)
            return self._id

    @staticmethod
    def find_by_id(scan_id: str) -> Optional['Scan']:
        """Trouve un scan par son ID"""
        try:
            scan_data = db.scans.find_one({'_id': ObjectId(scan_id)})
            if scan_data:
                return Scan(
                    _id=str(scan_data['_id']),
                    target=scan_data['target'],
                    scan_type=scan_data['scan_type'],
                    user_id=scan_data.get('user_id'),
                    status=scan_data['status'],
                    results=scan_data['results']
                )
        except Exception:
            return None
        return None

    @staticmethod
    def find_by_user(user_id: str, limit: int = 10) -> List['Scan']:
        """Trouve tous les scans d'un utilisateur"""
        scans_data = db.scans.find(
            {'user_id': user_id}
        ).sort('created_at', -1).limit(limit)

        return [
            Scan(
                _id=str(scan['_id']),
                target=scan['target'],
                scan_type=scan['scan_type'],
                user_id=scan['user_id'],
                status=scan['status'],
                results=scan['results']
            ) for scan in scans_data
        ]

    def to_dict(self) -> Dict[str, Any]:
        """Convertit le scan en dictionnaire"""
        return {
            'id': str(self._id) if self._id else None,
            'target': self.target,
            'scan_type': self.scan_type,
            'user_id': self.user_id,
            'status': self.status,
            'results': self.results,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def update_status(self, status: str, results: Optional[Dict] = None) -> None:
        """Met à jour le statut et les résultats du scan"""
        self.status = status
        if results:
            self.results = results
        self.updated_at = datetime.utcnow()
        self.save()