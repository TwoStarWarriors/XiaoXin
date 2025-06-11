ose all;clear all;clc

AA=xlsread(['E:\������ѧϰ\�о���\�����ݿ��������ļ���������\ģ��������\Vehicle1_0809_��������.xlsx']);%%
    A=AA(1:5470,1:100);%%%%ѡ�����ݷ�Χ��1-5��;%%%%ѡ�����ݷ�Χ��1-5��
for N=100
    numX=size(A,1);
for j=1:1:numX-N+1%%%%%%%%%%迭代循环的次�?
      k=1;
    for i=j:1:N+j-1
           C(k,:)=A(i,:);
           k=k+1;
       end
        B(j,:)=xiang_nong_max(C);
end
        h=std(B,0,2);%每行的标准差
B=B-repmat(mean(B,2),1,size(B,2));%减去平均�?
for m=1:numX-N+1
    for n=1:100
        B(m,n)=B(m,n)/h(m,1);%
    end
end
D=abs(B)
xlswrite(['E:\������ѧϰ\�о���\�����ݿ��������ļ���������\ģ��������\Vehicle1_0809_��������MOSE.xlsx'],B); 
xlswrite(['E:\������ѧϰ\�о���\�����ݿ��������ļ���������\ģ��������\Vehicle1_0809_��������MOSEAC.xlsx'],D); 
%figure
%plot(D) 
%saveas(gcf,['D:\桌面\燃料电池数据\鸿芯GI电堆水管理数据汇总\900mA-247.5A（先试一下）\4.空气计量比\测试台数据\模拟故障-膜干-AC-',int2str(N),],'jpg');
end


function H=xiang_nong_max(DATA)
a=size(DATA,1);b=size(DATA,2);
MAX=max(max(DATA));
MIN=min(min(DATA));
c=50;%%%%%%%%���ֵ������%%%%%%%%
ABS=(MAX-MIN)/c;
C=zeros(c,b);%%%%%%%%%�������ÿ�����������%%%%%%%%%
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

