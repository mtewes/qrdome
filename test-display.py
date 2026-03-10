import tm1637


CLK = 6
DIO = 5

tm = tm1637.TM1637(clk=CLK, dio=DIO)

tm.brightness(2)

# show "123"
tm.number(123)


