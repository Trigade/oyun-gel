class StateManager:
    def __init__(self):
        self._stack = [] #Aktif durumlar yığını

    @property
    def active(self):
        return self._stack[-1] if self._stack else None #En üstteki durum (Boşsa None)

    def push(self,new_state):
        self._stack.append(new_state) #Mevcut durumu duraklat ve yeni durumu üstüne ekle
        new_state.enter()

    def pop(self): #Üstteki durumu çıkar; altındaki tekrar aktif olur
        if self._stack:
            top = self._stack.pop()
            top.exit()

    def change(self,new_state):#Üstteki durumu çıkarıp yerine yenisini koy.
        if self._stack:
            self.pop()
        self.push(new_state)