clear all
format compact
clc;
excel_path=  'E:\工作与学习\研究生\2022数字汽车大赛\2022年数字汽车大赛创新题二数据\LB_47';
%for name=
    x_all=xlsread([excel_path,'part-00000-656083c2-99c3-4188-a9e0-df50bfdfaca6-c000.xlsx']);
   a=size(Xa,1);b=size(Xa,2);
   x_all=Xa(1:6241,2:101);%%%%选定数据范围的1-5列
    cell_no=100
res = zeros(20,cell_no);

for m=10
    for col = 1:cell_no
        sequence = x_all(:,col); 
        fe=FE(sequence, m);
        res(m,col)=fe;
    end
end

h=std(res,0,2);%
res=res-repmat(mean(res,2),1,size(res,2));%

for m=10
    for n=1:cell_no
        res(m,n)=res(m,n)/h(m,1);%
    end
end
xlswrite(['E:\工作与学习\研究生\大数据课题组论文及工作内容\模糊熵论文\全年数据\mfe\MFE0210.xlsx'],res);

function fe = FE(sequence, m)
    r = 0.2;
    n = length(sequence);
    result = zeros(1,2);
    for j=1:2
        m=m+j-1;
        phi = zeros(1, n-m);
        dataMat = segmentSeq(sequence, m);
        dataMat = dataMat-repmat(mean(dataMat), m, 1);     
        for i = 1:n-m+1
            tempMat =dataMat; 
            tempMat(:,i)=[];
            dij = max(abs(tempMat - repmat(dataMat(:,i), 1,n-m)));
            D = exp(-(dij.^2)/r);
            phi(i) = sum(D)/(n-m-1);
        end 
        result(j) = sum(phi)/(n-m)+eps;
    end
    fe = log(result(1))-log(result(2));
end
function E = segmentSeq(sequence, m)    
    n = length(sequence);
    E = sequence(1:m);
    for i = 1:n-m
        New_ind = 1+i:m+i;
        E = [E,sequence(New_ind)];
    end        
end