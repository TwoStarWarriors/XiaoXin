function H=xiang_nong_max(DATA)
a=size(DATA,1);b=size(DATA,2);
MAX=max(max(DATA));
MIN=min(min(DATA));
c=50;%%%%%%%%所分得类别数%%%%%%%%
ABS=(MAX-MIN)/c;
C=zeros(c,b);%%%%%%%%%用来存放每个区间的数字%%%%%%%%%
for m=1:1:b
    for n=1:1:a
        for i=1:1:c
            if DATA(n,m)>=MIN+(i-1)*ABS&&DATA(n,m)<=MIN+i*ABS
               C(i,m)=C(i,m)+1;
            end
        end
    end
end
C;
for i=1:1:b
    D=0;
    for j=1:1:c
        D=C(j,i)+D;
    end
        SUM(i)=D;
end
SUM;
for j=1:1:b
    for i=1:1:c
        N(i,j)=C(i,j)/SUM(j);
        shannon(i,j)=-N(i,j)*log2(N(i,j));
        if N(i,j)==0
            shannon(i,j)=0;
        end
    end
    shannon;
    E=0;
    for i=1:1:c
        E=E+shannon(i,j);
    end
    H(j)=E;
end
end            



