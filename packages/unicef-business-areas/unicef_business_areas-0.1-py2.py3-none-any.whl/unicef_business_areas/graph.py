import logging

logger = logging.getLogger(__name__)


class SyncResult:
    def __init__(self, keep_records=False):
        """
        :param keep_records: if True keep track of record istances
        """
        self.created = []
        self.updated = []
        self.skipped = []
        self.keep_records = keep_records

    def log(self, *result):
        if len(result) == 2:
            obj = {True: result[0],
                   False: result[0].pk}[self.keep_records]
            if result[1]:
                self.created.append(obj)
            else:
                self.updated.append(obj)
        else:
            self.skipped.append(result)

    def __add__(self, other):
        if isinstance(other, SyncResult):
            ret = SyncResult()
            ret.created.extend(other.created)
            ret.updated.extend(other.updated)
            ret.skipped.extend(other.skipped)
            return ret
        else:
            raise ValueError("Cannot add %s to SyncResult object" % type(other))

    def __repr__(self):
        return f"<SyncResult: {len(self.created)} {len(self.updated)} {len(self.skipped)}>"

    def __eq__(self, other):
        if isinstance(other, SyncResult):
            return self.created == other.created and self.updated == other.updated and self.skipped == other.skipped
        return False
