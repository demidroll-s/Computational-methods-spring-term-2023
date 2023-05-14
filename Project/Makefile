FILE='test/test.txt'
VAR=$(shell cat ${FILE})

all: $(VAR) clean

main_bsm: main_bsm.o bsm.o matlib.o 
	g++ main_bsm.o bsm.o matlib.o -o main_bsm
	./main_bsm

main_bsm.o: main_bsm.cpp
	g++ -c main_bsm.cpp

bsm.o: bsm.cpp
	g++ -c bsm.cpp

main_delta: main_hedging.o delta_hedging.o bsm.o matlib.o call_option.o continuous_time_option.o continuous_time_option_base.o monte_carlo.o
	g++ main_hedging.o delta_hedging.o bsm.o matlib.o call_option.o continuous_time_option.o continuous_time_option_base.o monte_carlo.o -o main_delta
	./main_delta

main_hedging.o: main_hedging.cpp
	g++ -c main_hedging.cpp

delta_hedging.o: delta_hedging.cpp
	g++ -c delta_hedging.cpp

matlib.o: matlib.cpp
	g++ -c matlib.cpp

call_option.o: call_option.cpp
	g++ -c call_option.cpp

continuous_time_option.o: continuous_time_option.cpp
	g++ -c continuous_time_option.cpp

continuous_time_option_base.o: continuous_time_option_base.cpp
	g++ -c continuous_time_option_base.cpp

monte_carlo.o: monte_carlo.cpp
	g++ -c monte_carlo.cpp

clean:
	rm -rf *.o main