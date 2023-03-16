LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY irtest IS
PORT(ir:  IN  STD_LOGIC;
     led: OUT STD_LOGIC);
END irtest;

ARCHITECTURE behavior OF irtest IS
BEGIN
    led <= ir;

END behavior;
