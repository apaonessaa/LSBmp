class StrategyImpl:
    @staticmethod
    def is_valid(value: int):
        # value : 255 = x : 100%
        return 0 <= value <=255
    
    @staticmethod
    def get_factor(value: int):
        # value : 255 = x : 100%
        if not StrategyImpl.is_valid(value):
            raise ValueError('Error@Strategy: the value is not valid.')
        return value * 100 // 255 if value>0 else 0
    
    # (1) strategy : LSB substitution if factor(src_value) > accuracy then 1 else 0
    @staticmethod
    def substitution(x, y, accuracy):
        factor = StrategyImpl.get_factor(y)
        return x & 0xFE if factor < accuracy else x | 0x01
    
    # (2) strategy : LSB substitution if factor(src_value) > accuracy then 1 else pass
    @staticmethod
    def substitution2(x, y, accuracy):
        factor = StrategyImpl.get_factor(y)
        return x | 0x01 if factor >= accuracy else x
    
class Strategy:
    method =None
    accuracy: int =0

    def set_accuracy(self, accuracy: int):
        if accuracy < 0 or accuracy>100:
            raise ValueError('Error@Strategy: the accuracy is not valid.')
        self.accuracy = accuracy
        return self

    def set_strategy(self, method):
        if method is None:
            raise ValueError('Error@Strategy: the method is null.')
        self.method = method
        return self
    
    def apply(self, x, y):
        return self.method(x,y,self.accuracy)
        