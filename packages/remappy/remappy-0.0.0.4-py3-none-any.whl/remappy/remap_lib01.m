##
## Collection of functions used in remap
##

## This file is part of REMAP.

## REMAP is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by the
## Free Software Foundation; either version 2, or (at your option) any
## later version.

## REMAP is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
## FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
## for more details.

## You should have received a copy of the GNU General Public License
## along with Octave; see the file COPYING.  If not, write to the Free
## Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
## 02110-1301, USA.


# par.lib_name= mfilename("fullpath");
fprintf(2,"loading %s\n", mfilename("fullpath"));

function print_usage()
  fprintf(2,"\n\n Usage remap.m driverfile.rmp \n\n");
  fprintf(2," Options:\n\n");
  fprintf(2," -g : display graphical results\n");
  fprintf(2," -d : print diagnostics data\n");
  fprintf(2," -h : print options\n\n");
end

function [str] = my_deblank(str)
% removes leading and trailing blanks

if (isempty(str));
else
  k =1;
  cond=' ';
  val=str(1);
  while (strcmp(cond,val) && length(str)>k)
    val=str(k);
    k = k+1;
  endwhile
  str(1:k-1)=[];
  str=deblank(str);
endif
endfunction

function [str] = my_split(str,splitstr,element)
  
  if nargin == 2
    element=1;
  endif
  
  k = strfind(str, splitstr);
  a = length(k);
  if (isempty(k));
  elseif (element == 1)
    str=str(1 : k(1)-1);  
  elseif (element < a+1)
    str=str((k(element-1)+1) : k(element)-1);
  elseif (element ==  a+1)
    str=str((k(element-1)+1) : end);  
elseif (element>a+1);
  printf('illegal input\n');
endif
  
endfunction

function sub_str = my_substr(str,beg,len)

  if (nargin == 2)
    sub_str = str(beg:end);
else
  sub_str = str(beg : (beg + len - 1));
endif
endfunction


function cr = cread(fsp) 
  a=0;
  while ~a
    cr=fgets(fsp); 
    if (strfind(cr,'#') > 2)
	fprintf(2,'\ninput error - comment sign in the middle of the line!');
	fprintf(2,'\n');
	error('REMAP input file error');	
    endif
	a= (my_substr(cr,1,1) ~= ' ') && (my_substr(cr,1,1) ~= '#') && (isspace(my_substr(cr,1,1)) ~= 1) ;
	cr=my_substr(cr,1,size(cr,2)-1);
	cr=my_deblank(cr);
   endwhile
endfunction



function [c,r] = input_f(fr)
##read input files 
## version test
s = cread(fr);
  if (strcmp(s,'0.1') == 0)
    fprintf(2,'\n wrong version: %s, 0.1 expected\n',s);
    fprintf(2,'\n');
    error('REMAP input file error');
  endif

				% output setup

  c.name_o=cread(fr);
  c.imax=str2num(cread(fr));
  c.z=str2num(cread(fr));
  c.offset=str2num(cread(fr));
  c.z=c.z-c.offset;
  c.depth=c.offset+[0:c.imax-1].*c.z./(c.imax-1);
  c.ref=str2num(cread(fr));
  c.prec=str2num(cread(fr));
  
  for i=1:6
    c.bc(i,:)=str2num(cread(fr));
  endfor

  c.bc(2,1)=c.bc(1,1)/((1000+c.bc(2,1))*c.ref/1000+1);
  c.bc(4,1)=c.bc(3,1)/((1000+c.bc(4,1))*c.ref/1000+1);
  c.bc(6,1)=c.bc(5,1)/((1000+c.bc(6,1))*c.ref/1000+1);
  c.bc(2,3)=c.bc(1,3)/((1000+c.bc(2,3))*c.ref/1000+1);
  c.bc(4,3)=c.bc(3,3)/((1000+c.bc(4,3))*c.ref/1000+1);
  c.bc(6,3)=c.bc(5,3)/((1000+c.bc(6,3))*c.ref/1000+1);

  c.steady=cread(fr);

  % check input data consistency

  if (c.bc(1,2) == 3) && (str2num(my_split(c.steady,' ',1))~=Inf)
    fprintf(2,'\n mistake in the input file: non-steady problem must have fixed boundary!\n');
    fprintf(2,'\n');
    error('REMAP input file error');
  endif

  for i=2:6
    if (c.bc(i,2) == 3)
      fprintf(2,'\n mistake in the input file: free boundary is only allowed for total my_substrate!\n');
  fprintf(2,'\n');
   error('REMAP input file error');
    endif
  endfor
  
  c.prop.p=cread(fr);   % porosity
  c.prop.t=cread(fr);   % temperature
  c.prop.c=cread(fr);   % consumption
  c.prop.a=cread(fr);   % alpha
  c.prop.s=cread(fr);   % sedimentation
  c.prop.o=cread(fr);   % omega
  c.prop.ds=cread(fr);  % dif_sub
  c.prop.dp=cread(fr);  % dif_product

  if (c.prop.s < 0) 
    fprintf(2,'\n mistake in the input file: sedimentation rate should be above zero!\n');
  fprintf(2,'\n');
  error('REMAP input file error');
  endif

  c.lim=str2num(cread(fr));

  c.beta=str2num(cread(fr));
  c.epsilon=str2num(cread(fr));
  c.jmax=str2num(cread(fr));
  c.dt=str2num(cread(fr));
  c.dif=str2num(cread(fr));
  c.fia=str2num(cread(fr));
  c.name_p=cread(fr);

  if (c.bc(1,2) ~=3) && (c.dif~=0)
    fprintf(2,'warning: step for lower boundary iteration should be 0 when fixed boundary is used\n');
    c.dif=0;
  endif

  fclose (fr);

%reading data files
  
  if (my_substr(c.prop.p,1,1) == 'F')
    r.phi = read_f(c.prop.p,c.offset);
    else
    if (my_substr(c.prop.p,1,1) ~= 'E') && (my_substr(c.prop.p,1,1) ~= 'C')
      fprintf(2,'\n mistake in the input file: porosity data driver should start with F, E or C\n');
     fprintf(2,'\n');
      error('REMAP input file error');
    endif
    r.phi = 0;  
  endif

  if (my_substr(c.prop.t,1,1) == 'F')
    r.temp = read_f(c.prop.t,c.offset);
  else
    if (my_substr(c.prop.t,1,1) ~= 'E') && (my_substr(c.prop.t,1,1) ~= 'C')
      fprintf(2,'\n mistake in the input file: temperature data driver should start with F, E or C\n');
      fprintf(2,'\n');
      error('REMAP input file error');
    endif
    r.temp = 0;  
  endif

				% for now assume velocities are only depend on porosity

  r.omega = 0; 
  r.sed = 0; 
  r.diff_sub = 0;  
  r.diff_prod = 0;  

  if (length(str2num(c.prop.s))== 1) 
    c.prop.o=strrep('E V.*par.phi(c.imax)./par.phi','V',[c.prop.s '+' c.prop.o]);
    if (my_substr(c.prop.p,1,1) ~= 'C')
      c.prop.s=strrep('E V.*(1-par.phi(c.imax))./(1-par.phi)','V',c.prop.s);
    else
      c.prop.s=strrep('C V','V',c.prop.s); 
    endif
  else
    c.prop.o=strrep(strrep('E V.*P./par.phi','V',[my_split(c.prop.s,' ',1) ' + ' c.prop.o]),'P',my_split(c.prop.s,' ',2));
    if (my_substr(c.prop.p,1,1) ~= 'C')
      c.prop.s=strrep(strrep('E V.*P./(1-par.phi)','V',my_split(c.prop.s,' ',1)),'P',['(1-' my_split(c.prop.s,' ',2) ')']);
    else
      c.prop.s=strrep('C V','V',c.prop.s); 
    endif
  endif

  if (length(str2num(c.prop.ds)) == 1) 
    c.prop.ds=strrep(c.prop.ds,c.prop.ds,['C ' c.prop.ds]);
    c.prop.dp=strrep(c.prop.dp,c.prop.dp,['C ' c.prop.dp]);
  else
    c.prop.ds=strrep(strrep('E ((m0+m1.*par.temp).*1e-10)./(1-log(par.phi.^2))','m0',my_split(c.prop.ds,' ',1)),'m1',my_split(c.prop.ds,' ',2));
    c.prop.dp=strrep(strrep('E ((m0+m1.*par.temp).*1e-10)./(1-log(par.phi.^2))','m0',my_split(c.prop.dp,' ',1)),'m1',my_split(c.prop.dp,' ',2));
  endif


  if (my_substr(c.prop.c,1,1) == 'F')
    r.con = read_f(c.prop.c,c.offset);
  else
    if (my_substr(c.prop.c,1,1) ~= 'E') && (my_substr(c.prop.c,1,1) ~= 'C')
      fprintf(2,'\n mistake in the input file: consumption data definition should start with F, E or C\n');
      fprintf(2,'\n');
      error('REMAP input file error');
    endif
    r.con = 0;  
  endif

  if (my_substr(c.prop.a,1,1) == 'F')
    r.alpha = read_f(c.prop.a,c.offset);
  else
    if (my_substr(c.prop.a,1,1) ~= 'E') && (my_substr(c.prop.a,1,1) ~= 'C')
      fprintf(2,'\n mistake in the input file: fractionation factor data driver should start with F, E or C\n');
      fprintf(2,'\n');
      error('REMAP input file error');
    endif
    r.alpha = 0;  
  endif
endfunction

function param = interp_f(r,v,c,param,pr,par)

  if (my_substr(pr,1,1) == 'F')
    x=floor(r.d/c.dz)+1;
  
    if (x(1)<=c.imax)
      v(1,[1:x(1)])=r.a(1);
      v(2,[1:x(1)])=r.b(1);
      i=2;
      while (i<r.l) && (x(i)<=c.imax)
	if (x(i-1)~=x(i))
	  v(1,[x(i-1)+1:x(i)])=r.a(i);
	  v(2,[x(i-1)+1:x(i)])=r.b(i);
	endif
	i=i+1;
      endwhile
      v(1,[x(i-1)+1:c.imax])=r.a(i);
      v(2,[x(i-1)+1:c.imax])=r.b(i); 
    else
      v(1,[1:c.imax])=r.a(1);
      v(2,[1:c.imax])=r.b(1);
    endif
    param= v(1,:).*([0:c.imax-1].*c.dz)+v(2,:);
  elseif (my_substr(pr,1,1) == 'E')
    ## vectorize is depreciated
    ## param=eval(vectorize(strrep(my_substr(pr,3),'Z','c.depth')));
    param=eval(strrep(my_substr(pr,3),'Z','c.depth'));
  else
    param(:)=str2num(my_substr(pr,3));
  endif
endfunction

function r = read_f(k,offset)
  
  fp=fopen([pwd,'/',my_substr(k,3)],'rt');
  
  if  (fp<0)
    fprintf(2,'\n File %s could not be read\n',[pwd,'/',my_substr(k,3)]);
  
    fprintf(2,'\n');
    error('REMAP file error');
    fclose(fp);
  else
    fprintf(2,'Reading data from %s\n',[pwd,'/',my_substr(k,3)]);
  endif
  
  fgets(fp);
  
  
  [my_a,count] = fscanf(fp,'%g, %g');
  my_a = reshape(my_a,2,count/2)';
  r.d=my_a(:,1);
  r.val=my_a(:,2);
  r.d=r.d-offset;
  r.b=zeros(count/2,1);
  r.a=zeros(count/2,1);
  
  r.a([2:length(r.val)])=diff(r.val)./diff(r.d);
  r.b([2:length(r.val)])=r.val([1:end-1])-r.a([2:end]).*r.d([1:end-1]);  
  r.l = length(r.d);
  r.a(1)=r.a(2);
  r.b(1)=r.b(2);
  
  
  r.l = length(r.d);
  r.a(1)=r.a(2);
  r.b(1)=r.b(2);
endfunction


function [par,c,conc] = solver_d(r,c,par,v,matr,conc,func,ind)

  conc(1,:) = conc(1,:) .* (conc(1,:) > 0); ## avoid negative concentrations
  matr.d(1) = c.bc(ind,1);
  if (c.bc(ind,2)==1)             %dirichlet  boundary
    matr.d(c.imax) = c.bc(ind,3);   
    matr.c(c.imax)=1;
    matr.c(2.*c.imax-1)=0.;
  else                             %neumann
    matr.d(c.imax) = c.bc(ind,4);
    matr.c(c.imax)=1./c.dz;
    matr.c(2.*c.imax-1)=-1./c.dz;
  endif


  matr.c([2:c.imax-1])=-2 .* par.ds(floor((ind+1)/2),[2:c.imax-1]) ./c.dz./c.dz  .*c.beta(2)- 1/c.dt*(1+c.beta(1))-2.*par.sigma(floor((ind+1)/2),[2:c.imax-1]).*par.omega(floor((ind/5))+1,[2:c.imax-1])./2./c.dz.*c.beta(2);
matr.c([c.imax+1:2.*c.imax-2])=c.beta(2).*(par.ds(floor((ind+1)/2),[2:c.imax-1]) ./c.dz./c.dz + (1+par.sigma(floor((ind+1)/2),[2:c.imax-1])).*par.omega(floor((ind/5))+1,[2:c.imax-1]) ./2./c.dz -(par.ds(floor((ind+1)/2),[3:c.imax]) - par.ds(floor((ind+1)/2),[1:c.imax-2]))./4./c.dz./c.dz - par.ds(floor((ind+1)/2),[2:c.imax-1]) ./ par.phi([2:c.imax-1]) .* (par.phi([3:c.imax])-par.phi([1:c.imax-2]))./4./c.dz./c.dz);
matr.c([2.*c.imax+1:3*c.imax-2])=c.beta(2).*(par.ds(floor((ind+1)/2),[2:c.imax-1]) ./c.dz./c.dz - (1-par.sigma(floor((ind+1)/2),[2:c.imax-1])).*par.omega(floor((ind/5))+1,[2:c.imax-1]) ./2./c.dz +(par.ds(floor((ind+1)/2),[3:c.imax]) - par.ds(floor((ind+1)/2),[1:c.imax-2]))./4./c.dz./c.dz + par.ds(floor((ind+1)/2),[2:c.imax-1]) ./ par.phi([2:c.imax-1]) .* (par.phi([3:c.imax])-par.phi([1:c.imax-2]))./4./c.dz./c.dz);
      

      matr.m=sparse(matr.a,matr.b,matr.c,c.imax,c.imax);

	% setting RHS vector

	matr.d([2:c.imax-1])=-(1+2*c.beta(1)).*conc(ind,[2:c.imax-1]) ./c.dt + eval(func).*((c.lim(1)==0)+(c.lim(1)~=0).*conc(1,[2:c.imax-1]) ./(conc(1,[2:c.imax-1]) + c.lim(1)+(conc(1,[2:c.imax-1])==0))).*par.f([2:c.imax-1])+c.beta(1).*conc(12+ind,[2:c.imax-1])./c.dt-(1-c.beta(2)).*((conc(ind,[3:c.imax])-conc(ind,[1:c.imax-2])).*(par.ds(floor((ind+1)/2),[3:c.imax]) - par.ds(floor((ind+1)/2),[1:c.imax-2]))./4./c.dz./c.dz+par.ds(floor((ind+1)/2),[2:c.imax-1]).*(conc(ind,[3:c.imax])-2.*conc(ind,[2:c.imax-1])+conc(ind,[1:c.imax-2]))./c.dz./c.dz+par.ds(floor((ind+1)/2),[2:c.imax-1])./par.phi([2:c.imax-1]).*(conc(ind,[3:c.imax])-conc(ind,[1:c.imax-2])).*(par.phi([3:c.imax])-par.phi([1:c.imax-2]))./4./c.dz./c.dz-par.omega(floor((ind/5))+1,[2:c.imax-1]).*(conc(ind,[3:c.imax])-conc(ind,[1:c.imax-2]))./2./c.dz);

				% solving linear equation system

  conc(ind,:)=(matr.m\matr.d')';
  conc(12+ind,:)=conc(6+ind,:);
  conc(6+ind,:)=conc(ind,:);  

endfunction

function [par,c,conc] = solver_it(r,c,par,v,matr,conc,func,ind)


  fprintf(2,'Calculating species %i\n',ind);

  % total substrate concentration calculation
  corr=1000;
  j=0;
  k=0;
  my_b=0;
  if (ind == 2) || (ind==4)
    epsilon_c = c.epsilon(3);
  else
    epsilon_c = c.epsilon(2);
  endif

  matr.d(1) = c.bc(ind,1);
  if (c.bc(ind,2)==1) || (c.bc(ind,2)==3)    %dirichlet or free boundary
    matr.d(c.imax) = c.bc(ind,3);   
    matr.c(c.imax)=1;
    matr.c(2.*c.imax-1)=0.;
  else                             %neumann
    matr.d(c.imax) = c.bc(ind,4);
    c.dz=c.z/(c.imax-1);
    matr.c(c.imax)=1./c.dz;
    matr.c(2.*c.imax-1)=-1./c.dz;
  endif

  my_a = 0;
  while (~my_a)
    conc(1,:) = conc(1,:) .* (conc(1,:) > 0); ## make sure we have no negative
    ## concentrations. Important for the monod limter term
    corr=1000;
    c.dz=c.z/(c.imax-1);
    c.depth=c.offset+[0:c.imax-1].*c.dz;
    j=j+1;
      
    %interpolation
    if (ind==1)
      par.phi=interp_f(r.phi,v,c,par.phi,c.prop.p,par);
      par.temp=interp_f(r.temp,v,c,par.temp,c.prop.t,par);
      par.omega(1,:)=interp_f(r.omega,v,c,par.omega(1,:),c.prop.o,par);
      par.ds(1,:)=interp_f(r.diff_sub,v,c,par.ds(1,:),c.prop.ds,par);
      par.f=interp_f(r.con,v,c,par.f,c.prop.c,par);

      if (c.fia ~= 0)
	par.sigma(:)=coth(par.omega(1,:).*c.dz./2./par.ds(1,:))-1./(par.omega(1,:).*c.dz./2./par.ds(1,:));
      elseif (sum(par.omega(1,:).*c.dz./2./par.ds(1,:)>1) > 0)
	fprintf(2,'\n Peclet number above 1. You might want to consider switching Fiadero scheme on');
	fprintf(2,'\n');
      error('REMAP solver warning');
      endif
    endif
    
    % setting matrix for the solver
    matr.c([2:c.imax-1])=-2 .* par.ds(floor((ind+1)/2),[2:c.imax-1]) ./c.dz./c.dz  .*c.beta(2)- 1/c.dt*(1+c.beta(1))-2.*par.sigma([2:c.imax-1]).*par.omega(floor((ind/5))+1,[2:c.imax-1])./2./c.dz.*c.beta(2);
      matr.c([c.imax+1:2.*c.imax-2])=c.beta(2).*(par.ds(floor((ind+1)/2),[2:c.imax-1]) ./c.dz./c.dz + (1+par.sigma([2:c.imax-1])).*par.omega(floor((ind/5))+1,[2:c.imax-1]) ./2./c.dz -(par.ds(floor((ind+1)/2),[3:c.imax]) - par.ds(floor((ind+1)/2),[1:c.imax-2]))./4./c.dz./c.dz - par.ds(floor((ind+1)/2),[2:c.imax-1]) ./ par.phi([2:c.imax-1]) .* (par.phi([3:c.imax])-par.phi([1:c.imax-2]))./4./c.dz./c.dz);
      matr.c([2.*c.imax+1:3*c.imax-2])=c.beta(2).*(par.ds(floor((ind+1)/2),[2:c.imax-1]) ./c.dz./c.dz - (1-par.sigma([2:c.imax-1])).*par.omega(floor((ind/5))+1,[2:c.imax-1]) ./2./c.dz +(par.ds(floor((ind+1)/2),[3:c.imax]) - par.ds(floor((ind+1)/2),[1:c.imax-2]))./4./c.dz./c.dz + par.ds(floor((ind+1)/2),[2:c.imax-1]) ./ par.phi([2:c.imax-1]) .* (par.phi([3:c.imax])-par.phi([1:c.imax-2]))./4./c.dz./c.dz);
      
      matr.m=sparse(matr.a,matr.b,matr.c,c.imax,c.imax);
      
      k=0;
      conc(7,:)=0;%1;
      conc(8,:)=0;
      my_b=0;
      
      while (~my_b)
	conc(1,:) = conc(1,:) .* (conc(1,:) > 0); ## make sure there is no negative C
	k=k+1;
	corr=0.;

	% setting RHS vector
	matr.d([2:c.imax-1])=-(1+2*c.beta(1)).*conc(ind,[2:c.imax-1]) ./c.dt + eval(func).*((c.lim(1)==0)+(c.lim(1)~=0).*conc(1,[2:c.imax-1]) ./(conc(1,[2:c.imax-1]) + c.lim(1)+(conc(1,[2:c.imax-1])==0))).*par.f([2:c.imax-1])+c.beta(1).*conc(8,[2:c.imax-1])./c.dt-(1-c.beta(2)).*((conc(ind,[3:c.imax])-conc(ind,[1:c.imax-2])).*(par.ds(floor((ind+1)/2),[3:c.imax]) - par.ds(floor((ind+1)/2),[1:c.imax-2]))./4./c.dz./c.dz+par.ds(floor((ind+1)/2),[2:c.imax-1]).*(conc(ind,[3:c.imax])-2.*conc(ind,[2:c.imax-1])+conc(ind,[1:c.imax-2]))./c.dz./c.dz+par.ds(floor((ind+1)/2),[2:c.imax-1])./par.phi([2:c.imax-1]).*(conc(ind,[3:c.imax])-conc(ind,[1:c.imax-2])).*(par.phi([3:c.imax])-par.phi([1:c.imax-2]))./4./c.dz./c.dz-par.omega(floor((ind/5))+1,[2:c.imax-1]).*(conc(ind,[3:c.imax])-conc(ind,[1:c.imax-2]))./2./c.dz);
	
	% solving linear equation system
	conc(ind,:)=(matr.m\matr.d')';
		  
	% convergence check
	if (ind == 2) || (ind == 4)
	  corr=sum(abs(((conc(ind-1,:)-conc(ind,:))./(conc(ind,:)+(conc(ind,:)==0))./c.ref-1.*(conc(ind,:)~=0)).*1000-conc(7,:)));
	  conc(8,:)=conc(7,:);
	  conc(7,:)=((conc(ind-1,:)-conc(ind,:))./(conc(ind,:)+(conc(ind,:)==0))./c.ref-1.*(conc(ind,:)~=0)).*1000.;
	else
	  corr=sum(abs(conc(ind,:)-conc(7,:)));
          conc(8,:)=conc(7,:);
	  conc(7,:)=conc(ind,:);
	endif
	my_b=(corr<epsilon_c) | (k>c.jmax(2));
      endwhile
      
      if (k>c.jmax(2)) 
	fprintf(2,'Excedeed maximum number of iteractions for convergence\n'); 
      end
      
      % free boundary location calculation
      if (c.bc(1,2) == 3) && (ind == 1)

	grad=(conc(ind,c.imax)-conc(ind,c.imax-1))/c.dz; 
	    
	if (c.epsilon(1)<0.)
	  if (grad>c.epsilon(1)+c.bc(ind,4))
	    if (c.dif>0.) 
	      c.dif=-c.dif/2.; 
	    endif
	  else
	    if (c.dif<0.) 
	      c.dif=-c.dif/2.;
	    endif
	  endif
	else
	  if (grad<c.epsilon(1)+c.bc(ind,4))
	    if (c.dif>0.) 
	      c.dif=-c.dif/2.; 
	    endif
	  else
	    if (c.dif<0.) 
	      c.dif=-c.dif/2.;
	    endif
	  endif
	endif
	c.z=c.z+c.dif; 
	fprintf(2,'Locating lower boundary (%i): Iteration %i gradient %g length %g\n',j,k,grad,c.z);
      endif
      my_a = (abs(c.dif)<c.epsilon(4)) | (j>c.jmax(1));
  endwhile
  
  if (j> c.jmax(1)) 
    fprintf(2,'Excedeed maximum number of iteractions while searching for lower boundary location');
    c.dif=0;
  endif
  fprintf(2,'Species %i completed (%i) iterations\n',ind,k);
endfunction

function [par,c,conc] = solver_nit(r,c,par,v,matr,conc,func,ind)
  fprintf(2,'Calculating species %i\n',ind);
  % total substrate concentration calculation

  j=0;
  
  matr.d(1) = c.bc(ind,1);
  if (c.bc(ind,2)==1) || (c.bc(ind,2)==3)    %dirichlet or free boundary
    matr.d(c.imax) = c.bc(ind,3);   
    matr.c(c.imax)=1;
    matr.c(2.*c.imax-1)=0.;
  else                             %neumann
    matr.d(c.imax) = c.bc(ind,4);
    c.dz=c.z/(c.imax-1);
    matr.c(c.imax)=1./c.dz;
    matr.c(2.*c.imax-1)=-1./c.dz;
  end
  
				% if not a free boundary c.dif==0!!
my_a = 0;

  while ~my_a
    conc(1,:) = conc(1,:) .* (conc(1,:) > 0); ## avoid negative concentrations
    c.dz=c.z/(c.imax-1);
    c.depth=c.offset+[0:c.imax-1].*c.z./(c.imax-1);
    j=j+1;

				%interpolation

    if (ind==1)

      par.phi=interp_f(r.phi,v,c,par.phi,c.prop.p,par);
      par.temp=interp_f(r.temp,v,c,par.temp,c.prop.t,par);
      par.omega(1,:)=interp_f(r.omega,v,c,par.omega(1,:),c.prop.o,par);
      par.ds(1,:)=interp_f(r.diff_sub,v,c,par.ds(1,:),c.prop.ds,par);
      par.f=interp_f(r.con,v,c,par.f,c.prop.c,par);

      if (c.fia ~= 0)

	par.sigma(:)=coth(par.omega(1,:).*c.dz./2./par.ds(1,:))-1./(par.omega(1,:).*c.dz./2./par.ds(1,:));

      elseif (sum(par.omega(1,:).*c.dz./2./par.ds(1,:)>1) > 0)
	fprintf(2,'\n Peclet number above 1. You might want to consider switching Fiadero scheme on');
	fprintf(2,'\n');
	error('REMAP solver warning');
      end
    end
    

				% setting matrix for the solver
    
    matr.c([2:c.imax-1])=-2 .* par.ds(floor((ind+1)/2),[2:c.imax-1]) ./c.dz./c.dz  .*c.beta(2)-2.*par.sigma([2:c.imax-1]).*(par.omega(floor((ind/5))+1,[2:c.imax-1]))./2./c.dz.*c.beta(2);
    matr.c([c.imax+1:2.*c.imax-2])=c.beta(2).*(par.ds(floor((ind+1)/2),[2:c.imax-1]) ./c.dz./c.dz + (1+par.sigma([2:c.imax-1])).*par.omega(floor((ind/5))+1,[2:c.imax-1]) ./2./c.dz -(par.ds(floor((ind+1)/2),[3:c.imax]) - par.ds(floor((ind+1)/2),[1:c.imax-2]))./4./c.dz./c.dz - par.ds(floor((ind+1)/2),[2:c.imax-1]) ./ par.phi([2:c.imax-1]) .* (par.phi([3:c.imax])-par.phi([1:c.imax-2]))./4./c.dz./c.dz);
    matr.c([2.*c.imax+1:3*c.imax-2])=c.beta(2).*(par.ds(floor((ind+1)/2),[2:c.imax-1]) ./c.dz./c.dz - (1-par.sigma([2:c.imax-1])).*par.omega(floor((ind/5))+1,[2:c.imax-1]) ./2./c.dz +(par.ds(floor((ind+1)/2),[3:c.imax]) - par.ds(floor((ind+1)/2),[1:c.imax-2]))./4./c.dz./c.dz + par.ds(floor((ind+1)/2),[2:c.imax-1]) ./ par.phi([2:c.imax-1]) .* (par.phi([3:c.imax])-par.phi([1:c.imax-2]))./4./c.dz./c.dz);

    matr.m=sparse(matr.a,matr.b,matr.c,c.imax,c.imax);
    
				% setting RHS vector

    matr.d([2:c.imax-1])=eval(func).*((c.lim(1)==0)+(c.lim(1)~=0).*conc(1,[2:c.imax-1]) ./(conc(1,[2:c.imax-1]) + c.lim(1)+(conc(1,[2:c.imax-1])==0))).*par.f([2:c.imax-1])-(1-c.beta(2)).*((conc(ind,[3:c.imax])-conc(ind,[1:c.imax-2])).*(par.ds(floor((ind+1)/2),[3:c.imax]) - par.ds(floor((ind+1)/2),[1:c.imax-2]))./4./c.dz./c.dz+par.ds(floor((ind+1)/2),[2:c.imax-1]).*(conc(ind,[3:c.imax])-2.*conc(ind,[2:c.imax-1])+conc(ind,[1:c.imax-2]))./c.dz./c.dz+par.ds(floor((ind+1)/2),[2:c.imax-1])./par.phi([2:c.imax-1]).*(conc(ind,[3:c.imax])-conc(ind,[1:c.imax-2])).*(par.phi([3:c.imax])-par.phi([1:c.imax-2]))./4./c.dz./c.dz-par.omega(floor((ind/5))+1,[2:c.imax-1]).*(conc(ind,[3:c.imax])-conc(ind,[1:c.imax-2]))./2./c.dz);

				% solving linear equation system
    
    conc(ind,:)=(matr.m\matr.d')';
		 
				% free boundary location calculation

    if (c.bc(1,2) == 3) && (ind == 1)

      grad=(conc(ind,c.imax)-conc(ind,c.imax-1))/c.dz; 

      if (c.epsilon(1)<0.)
	if (grad>c.epsilon(1)+c.bc(ind,4))
	  if (c.dif>0.) 
	    c.dif=-c.dif/2.; 
	  end
	else
	  if (c.dif<0.) 
	    c.dif=-c.dif/2.;
	  end
	end
      else
	if (grad<c.epsilon(1)+c.bc(ind,4))
	  if (c.dif>0.) 
	    c.dif=-c.dif/2.; 
	  end
	else
	  if (c.dif<0.) 
	    c.dif=-c.dif/2.;
	  end
	end
      end
      c.z=c.z+c.dif; 

      fprintf(2,'Locating lower boundary (%i):gradient %g length %g \n',j,grad,c.z);
      
    end
    my_a =  (abs(c.dif)<c.epsilon(4)) || (j>c.jmax(1));
  end
  
  if (j> c.jmax(1) )
    fprintf(2,'Excedeed maximum number of iteractions while searching for lower boundary location');
    c.dif=0;
  end 
  
  fprintf(2,'Species %i completed\n',ind);

endfunction











