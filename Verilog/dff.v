module dff(input clk, D,rst output Q
    );

always @(posedge clk or posedge rst)
begin
if(rst)
    Q <= 1'b0;
else
    Q <= D;
end
endmodule