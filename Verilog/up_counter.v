module up_counter(input clk, rst, output[31:0] counter
    );
reg [31:0] counter;
    
always @(posedge clk or posedge rst)
begin
if(rst)
 counter <= 32'd0;
else
 counter <= counter + 32'd1;
end 
endmodule
