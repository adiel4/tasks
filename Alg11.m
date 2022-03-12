Kyrg=dlmread('/home/adilet/Desktop/res.txt');
x=[16 18.4 20.4 22 24 26.4 31 33.4 36 37.4 39.4 42.4 48];
Days=['02.12.2015';'03.12.2015';'04.12.2015';'05.12.2015';'06.12.2015';'07.12.2015';'08.12.2015';'09.12.2015';'10.12.2015'];
Day=9;
y=Kyrg(93,:);
a=y(1);b=y(2);c=y(3);d=y(4);e=y(5);f=y(6);m=y(7);n=y(8);p=y(9);q=y(10);r=y(11);s=y(12);t=y(13);a1=1:11;a2=1:9;cd=d-c;de=e-d;ef=f-e;fm=m-f;mn=n-m;np=p-n;pq=q-p;qr=r-q;rs=s-r;st=t-s;j=a+a1*ab/12;j1=b+a2*bc/10;j2=c+a3*cd/8;j3=d+a2*de/10;j4=e+a1*ef/12;j5=f+a4*fm/23;j6=m+a1*mn/12;j7=n+a5*np/13;j8=p+a6*pq/7;j9=q+a2*qr/10;k=r+a7*rs/15;k1=s+a8*st/28;h=[16:0.2:48]';u=[a j b j1 c j2 d j3 e j4 f j5 m j6 n j7 p j8 q j9 r k s k1 t];x1=[16 18 20 22 24 26 28 30 32 34 36 38 40 42 44 46 48];y1=[u(1) u(11) u(21) u(31) u(41) u(51) u(61) u(71) u(81) u(91) u(101) u(111) u(121) u(131) u(141) u(151) u(161)];yi=interp1(x1,y1,h,'spline');
%         figure(1)%         plot(y,x,'o',yi,h,u,h);%         grid on%         set(gca,'Fontsize',12)%         xlabel('Temperature'); %         ylabel('Height,km');%         axis tight;%         title(Days(Day,1:10));%         saveas(figure(1),'Fig1.jpg');
Diap1=16;
Diap2=48;
Pred1=round((Diap1-15.8)/0.2);
Pred2=round((Diap2-15.8)/0.2);
h3=h(Pred1:Pred2);
yi3=yi(Pred1:Pred2);
SplineFit=fit(h3,yi3, 'smoothingspline', 'SmoothingParam',0.001);
spl2=SplineFit(h3);
%         figure(2)
%         plot(spl2,h3,yi3,h3);
%         legend({'Tspl','Tinterp'},'Location','southeast')
%         hold on   
        Wave_Diap2=40.8;
        Wave_Diap1=28.8;
        Volna=1;
%         plot(spl2,Wave_Diap1,'ko',spl2,Wave_Diap2,'ko');
%         hold off
%         grid on
%         grid minor
%         xlabel('Temperature'); 
%         ylabel('Height, km');
%         title(Days(Day,1:10));
%         axis tight;
%       saveas(figure(2),'Fig2.jpg');
    
sti=yi3-spl2;
sti1=sti./spl2;


sn=256;
dT = 'dT';
TIT=Days(Day,1:10);
Fs = 0.2;
wt = cwt(sti1,1:sn,'cmor,2-0.96');
h1=1;
s2=1:1:sn;
s1=s2*1.03*Fs;
figure(3)
    subplot(2,2,1); 
    plot(sti,h3);
    axis tight;
    grid on
    title(TIT); 
    xlabel(dT); 
    ylabel('h,km');
            subplot(2, 2, 3);
            wt1=abs(wt)';
            imagesc(s1,h3, wt1);
            colormap(jet);
            axis xy; 
            title(TIT); 
            xlabel('Wavelenght,km'); 
            ylabel('Height,km'); 
            x1 = mean(abs(wt), 2); 
                subplot(2, 2, 4);
                plot(s1, x1);                 
                grid on
                title(TIT); 
                xlabel('Wavelenght,km'); 
                ylabel('Amplitude');
                peak = findpeaks(x1);
                indexmax = find(peak(Volna) == x1);
                xmax=s1(indexmax);
                ymax=x1(indexmax);
                strmax=strcat(['Wavelenght= ',num2str(xmax)],'km');
                text(xmax,ymax,strmax,'HorizontalAlignment','left');
                
        subplot(2, 2, 2); 
        abs_wt=abs(wt);
        x2 = abs_wt(indexmax,:); 
        plot(x2,h3); 
        grid on
        title(TIT); 
        xlabel('Amplitude'); 
        ylabel('Height,km');
%         saveas(figure(3),'Fig3.jpg');

s13=diff(spl2)./diff(h3);
N21=9.8./spl2;
s14=[s13; s13(end)];
N22=(s14*(10^-3))+(9.8e-3);
N2=N21.*N22;


L1=round((Wave_Diap1-(Diap1-0.2))/0.2);
L2=round((Wave_Diap2-(Diap1-0.2))/0.2);
N=mean(N2(L1:L2));
ampl=max(x2);
DlVoln=xmax;
ae=(2*pi*9.8*ampl)/(xmax*1000*N);
w=(9.7e-5/2)*((2-ae)/(sqrt(1-ae)));

L=h3(end)-h3(1);
minT=1/sqrt(((h3(L2)-h3(L1))/DlVoln)-((0.2/DlVoln)^2));
mint=abs(sti);
[pks,locs]=findpeaks(mint(L1:L2));
min_ampl=min(pks);
Gamma=(yi3(L2)-yi3(L1))/(10*(h3(L2)-h3(L1)));

DiapVys=((DlVoln/min_ampl)^2+(0.2)^2)/DlVoln;

sti4=sti-mean(sti);
sti4=sti4.*sti4;
SmoSti=smooth(sti4,30);

PotEn=(9.8*9.8*SmoSti)./(2*N2.*spl2./spl2);
PotEn1=(9.8*9.8*sti4)./(2*N2.*spl2.*spl2);
SplineFit=fit(h,PotEn1, 'smoothingspline', 'SmoothingParam',0.001);
PotEnSpl=SplineFit(h);
[MaxPot, MaxPotHeightID]=findpeaks(PotEn1(L1:L2));
MaxPotHeight=Wave_Diap1+0.2*(MaxPotHeightID-1);
MeanPot=mean(PotEn1(L1:L2));
% Tabl2=[round(100*min_ampl)/100 round(100*minT)/100 Wave_Diap2 Wave_Diap1 Wave_Diap2-Wave_Diap1 round(100*ampl*1000)/100;round(100000*N)/10 round(100*DlVoln)/100 round(100*w*10000)/100 round(1000000*9.7e-5/w)/10000 round(100*sqrt(N)/w)/100 round(100*Gamma)/100];



index=find(MaxPot==max(MaxPot));
Energ=MaxPot(index);
EnergHeight=MaxPotHeight(index);
Tabl=[round(100*DlVoln)/100 Wave_Diap2 Wave_Diap1 round(100*minT)/100 Wave_Diap2-Wave_Diap1 round(10*DiapVys)/10 round(100*ampl*1000)/100 round(100000*N)/10 round(100*w*10000)/100 round(100*MeanPot)/100 round(100*Energ)/100 round(10*EnergHeight)/10 round(100*Gamma)/100 ];








%             figure(4)
%             subplot(2,1,1);
%             plot(N2,h3,'g',N2,h3(L1),'k.',N2,h3(L2),'k.','LineWidth',1.5);
%                 grid on
%             grid minor
%             xlabel('B-W frequency');
%             ylabel('Height, km');
%             axis tight;
%             title(TIT); 
%             subplot(2,1,2);
%             plot(sti1,h3,'r',sti1,h3(L1),'k.',sti1,h3(L2),'k.','LineWidth',1.5);
%                 grid on
%             grid minor
%             axis tight;
%             xlabel('dT/T');
%             ylabel('Height,km');
            title(Days(Day,1:10));
%     saveas(figure(4),'Fig4.jpg');
%     subplot(2,1,2);

%             figure(5)
%             plot(yi3,h3,'--',spl2,h3,spl2,h3(L1),'k.',spl2,h3(L2),'k.','LineWidth',1.5);
%             legend({'Tinterp','Tspl'},'Location','northwest')
%             grid on
%             grid minor
%             axis tight;
%             xlabel('Temperature');
%             ylabel('Height,km');
%             title(Days(Day,1:10));
%     saveas(figure(5),'Fig5.jpg');

    
    
    
%     
% figure(6)
% plot(h,sti4,h,sti,h,0,'LineWidth',1.5)
% ylabel('Temp variation')
% xlabel('Height,km')
% legend({'<deltaT^2>','deltaT'},'Location','northeast') 
% title(Days(Day,1:10));
% saveas(figure(6),'Fig6.jpg');



%         figure(7)
%         plot(h,PotEn1,h,PotEnSpl,h(L1),PotEn1,'k.',h(L2),PotEn1,'k.','LineWidth',1.5)
%         legend({'PotEn','PotEn(spl)'},'Location','northeast')
%         xlabel('Height,km')
%         ylabel('PotEn,J/kg')
%         title(Days(Day,1:10));
% saveas(figure(7),'Fig7.jpg');
