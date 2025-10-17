from datetime import datetime
from typing import Optional
from .exceptions import ValidationError


class Validator:

    @staticmethod
    def validate_text(
        text: str, field_name: str, max_length: int, allow_empty: bool = False
    ) -> str:
       
        if not isinstance(text, str):
            raise ValidationError(f"{field_name} must be string")
            
        text = text.strip()
        
        if not text and not allow_empty:
            raise ValidationError(f"{field_name} just not be emoty")
            
        if len(text) > max_length:
            raise ValidationError(
                f"{field_name}cant more then{max_length} charcter"
            )
            
        return text

    @staticmethod
    def validate_status(status: str) -> str:
   
        valid_statuses = {"todo", "doing", "done"}
        if status not in valid_statuses:
            raise ValidationError(
                f"stauts{', '.join(valid_statuses)} be"
            )
        return status

    @staticmethod
    def validate_deadline(deadline: Optional[str]) -> Optional[str]:
        
      
        if deadline is None:
            return None
            
        try:
            datetime.strptime(deadline, "%Y-%m-%d")
            return deadline
        except ValueError:
            raise ValidationError(
               
            )