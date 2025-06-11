ose all;clear all;clc

AA=xlsread(['E:\工作与学习\研究生\大数据课题组论文及工作内容\模糊熵论文\Vehicle1_0809_单个故障.xlsx']);%%
    A=AA(1:5470,1:100);%%%%选定数据范围的1-5列;%%%%选定数据范围的1-5列
for N=100
    numX=size(A,1);
for j=1:1:numX-N+1%%%%%%%%%%杩唬寰幆鐨勬鏁?
      k=1;
    for i=j:1:N+j-1
           C(k,:)=A(i,:);
           k=k+1;
       end
        B(j,:)=xiang_nong_max(C);
end
        h=std(B,0,2);%姣忚鐨勬爣鍑嗗樊
B=B-repmat(mean(B,2),1,size(B,2));%鍑忓幓骞冲潎鍊?
for m=1:numX-N+1
    for n=1:100
        B(m,n)=B(m,n)/h(m,1);%
    end
end
D=abs(B)
xlswrite(['E:\工作与学习\研究生\大数据课题组论文及工作内容\模糊熵论文\Vehicle1_0809_单个故障MOSE.xlsx'],B); 
xlswrite(['E:\工作与学习\研究生\大数据课题组论文及工作内容\模糊熵论文\Vehicle1_0809_单个故障MOSEAC.xlsx'],D); 
%figure
%plot(D) 
%saveas(gcf,['D:\妗岄潰\鐕冩枡鐢垫睜鏁版嵁\楦胯姱GI鐢靛爢姘寸鐞嗘暟鎹眹鎬籠900mA-247.5A锛堝厛璇曚竴涓嬶級\4.绌烘皵璁￠噺姣擻娴嬭瘯鍙版暟鎹甛妯℃嫙鏁呴殰-鑶滃共-AC-',int2str(N),],'jpg');
end


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

