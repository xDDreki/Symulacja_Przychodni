def czas(self):
    hours = 8 + self.env.now // 60
    minutes = self.env.now % 60
    if len(str(minutes)) == 1:
        return f"{hours}:0{minutes}"
    return f"{hours}:{minutes}"