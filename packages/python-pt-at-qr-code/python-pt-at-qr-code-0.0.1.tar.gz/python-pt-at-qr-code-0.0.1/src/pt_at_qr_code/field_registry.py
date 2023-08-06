class FieldRegistry:
  FIELDS = {
    'A': { 'human': 'seller_vat_number', 'type': 'string' },
    'B': { 'human': 'buyer_vat_number' , 'type': 'string' },
    'C': { 'human': 'buyer_country'    , 'type': 'string' },
    'D': { 'human': 'document_type'    , 'type': 'string' },
    'E': { 'human': 'document_status'  , 'type': 'string' },
    'F': { 'human': 'document_date'    , 'type': 'date'   },
  }

  def get_field(self, name):
    return self.FIELDS[name]
