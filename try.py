class car:
    def __init__(self,name,color,model,type):
        self.name = name
        self.color = color
        self.model = model
        self.type = type
    def car_info(self):
        print(f"name:{self.name},color:{self.color},model:{self.model},type:{self.type}")

c1 = car("toyota","white","crysta","suv")
c2 = car("mahindra","black","scorpio","4x4")
c1.car_info()
c2.car_info()
