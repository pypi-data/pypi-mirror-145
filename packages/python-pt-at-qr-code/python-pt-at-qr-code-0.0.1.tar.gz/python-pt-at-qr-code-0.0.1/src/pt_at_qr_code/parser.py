from .field_registry import FieldRegistry

class Parser:
  def __init__(self, human_readable_fields=False):
    self.human_readable_fields = human_readable_fields
    self.field_registry = FieldRegistry()

  def parse(self, string):
    string = 'A:500000000*B:123456789*C:PT*D:FT*E:N*F:20191124*G:NF 19A/789145*H: JL9DS4TT-789145*I1:PT- AC*I7:50.00*I8:9.00*L:1000.00*N:9.00*O:1059.00*Q:d8/K*R:9999'
    pairs = string.split('*')
    
    fields = {}
    for f in pairs:
      k, v = f.split(':')
      if self.human_readable_fields: 
        try:
          k = self.field_registry.get_field(k)['human']
        except Exception as e:
          pass

      fields[k] = v

    print(fields)
