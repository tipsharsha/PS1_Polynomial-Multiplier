`include "up_counter.v"
module upcounter_testbench();
reg clk, rst;
wire [31:0] counter;
    $dumpfile("h.vcd")
    $dumpvars(0,"up_counter_testbench")
up_counter dut(clk, rst, counter);
always #5 clk=~clk;
initial begin
rst=1;
#30;
rst=0;
end
endmodule