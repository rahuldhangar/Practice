%{
    Problem Statement:

    MATLAB language;

    Boyle's law of gases says that:
    P1V1 = P2V2

    Make a program (script) that calculates any of the 4 parameters, based on the elements that the user decides, that is:

    P1 = P2V2 / V1 - ask for the data that is needed. P2, V2, V1
    V1 = P2V2 / P1 - ask for the data that is needed. P2, V2, P1
    P2 = P1V1 / V2 - ask for the data that is needed. P1, V2, V1
    V2 = P1V1 / P2 - ask for the data that is needed. P1, P2, V1

    REMEMBER THAT FROM THAT ELECTION, THE REQUIRED VALUES ARE ASKED
%}

%{    
    Solution:
    MATLAB script to calculate the desired parameter value out of four (P1, V2, P2, V2)
    based on the values entered for other parameters
%}

fprintf("Enter parameter values below and leave the unknown parameter blank to calculate its value.\n");

P1 = input("Enter value of P1: ");
P2 = input("Enter value of P2: ");
V1 = input("Enter value of V1: ");
V2 = input("Enter value of V2: ");

if(isempty(P1))
    if( isempty(P2) || isempty(V1) || isempty(V2) )
        fprintf("Enter atleast any 3 parameters to calculate value of remaining one\n");
    else
        P1 = P2 * V2 / V1;
        fprintf("P1 = %f\n",P1);
    end
elseif( isempty(P2) )
    if( isempty(P1) || isempty(V1) || isempty(V2) )
        fprintf("Enter atleast any 3 parameters to calculate value of remaining one\n");
    else
        P2 = P1 * V1 / V2;
        fprintf("P2 = %f\n",P2);
    end
elseif( isempty(V1) )
    if( isempty(P1) || isempty(P2) || isempty(V2) )
        fprintf("Enter atleast any 3 parameters to calculate value of remaining one\n");
    else
        V1 = P2 * V2 / P1;
        fprintf("V1 = %f\n",V1);
    end
elseif( isempty(V2) )
    if( isempty(P1) || isempty(P2) || isempty(V1) )
        fprintf("Enter atleast any 3 parameters to calculate value of remaining one\n");
    else
        V2 = P1 * V1 / P2;
        fprintf("V2 = %f\n",V2);
    end
else
    fprintf("Enter any 3 parameters to calculate the value of 4th one.\n");
end