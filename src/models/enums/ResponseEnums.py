from enum import Enum

class ResponseSignal(Enum):
    FILE_VALIDATED_SUCESS = "file_validated_successfully"
    FILE_TYPE_NOT_SUPPORTED ="file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCESS = "file_upload_sucess"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    PROCESSING_SUCESS = "processing_sucess"
    PROCESSING_FAILED = "processing_failed"