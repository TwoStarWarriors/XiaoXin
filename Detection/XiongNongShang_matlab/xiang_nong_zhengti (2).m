close all;clear all;clc
AA=xlsread('C:\Users\bitcl.xls',1,'A:D');%%%%ѡ�����ݷ�Χ����
A=AA(:,[1:4]);%%%%ѡ�����ݷ�Χ��1-n��  
N=100;
numX=size(A,1);
for j=1:1:numX-N+1%%%%%%%%%%����ѭ���Ĵ���
      k=1;
    for i=j:1:N+j-1
           C(k,:)=A(i,:);
           k=k+1;
       end
        B(j,:)=xiang_nong_max(C); 
        ABN(j,:)=abs((B(j,:)-mean(B(j,:)))/std(B(j,:)));%%%%ÿһ�У�ÿ�鵥���أ����쳣ϵ��
end
figure%%%figure1
plot((1:numX),A(:,1),(1:numX),A(:,2),'k',(1:numX),A(:,3),'m',(1:numX),A(:,4),'r-')%%%%%%%%ԭ����
legend('cell 1','cell 2','cell 3','cell 4')
ylabel('Voltage/V');xlabel('Time/s');
figure%%%figure2
plot((1:j),B(:,1),(1:j),B(:,2),'k-',(1:j),B(:,3),'m-',(1:j),B(:,4),'r-')%%%%%%%%��ũ��ֵ
legend('cell 1','cell 2','cell 3','cell 4')
ylabel('Entropy');xlabel('Time/s')
figure%%%figure3
plot((1:j),ABN(:,1),(1:j),ABN(:,2),'k-',(1:j),ABN(:,3),'m-',(1:j),ABN(:,4),'r-')%%%%%%%%�쳣ϵ��ֵ
legend('cell 1','cell 2','cell 3','cell 4')
ylabel('Abnormal coefficient');xlabel('Time/s')
