%  REMAP Copyright (C) 2006 Boris Chernyavsky
% 

% This file is part of REMAP.

% REMAP is free software; you can redistribute it and/or modify it
% under the terms of the GNU General Public License as published by the
% Free Software Foundation; either version 2, or (at your option) any
% later version.

% REMAP is distributed in the hope that it will be useful, but WITHOUT
% ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
% FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
% for more details.

% You should have received a copy of the GNU General Public License
% along with Octave; see the file COPYING.  If not, write to the Free
% Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
% 02110-1301, USA.

%

function [c, conc, r, v, par] = start_remap(fn)

## modify this as needed
remap_version="REAMP version 0.11";
# remap_lib_location=("/home/uliw/user/remap-svn/remap/trunk/remap_code/");

##addpath (genpath (remap_lib_location));
# addpath(remap_lib_location);
# path()
# fprintf(2,'\n%s\n',remap_version);
remap_lib01;
  
try ## test if file
      fp=fopen(fn,'r');
      fprintf(2,'File %s is readable, fp=%g\n',fn,fp);
catch
  fprintf(2,'\n No such file %s\n',fn);
  fprintf(2,'\n')
  error('REMAP file error');
end
try ## test if remap file
  [c,r] = input_f(fp);
  fprintf(2,'Data read from %s\n',fn);
catch
  fprintf(2,'\n Error reading data from file %s\n',fn);
  fprintf(2,'\n');
  disp(lasterror);
  error('REMAP file error');
end
  
v=zeros(2,c.imax);
matr.a=zeros(1,3*c.imax-2)+1;
matr.b=zeros(1,3*c.imax-2)+1;
matr.c=zeros(1,3*c.imax-2);
matr.d=zeros(1,c.imax);
matr.m=zeros(c.imax,c.imax);
matr.m=sparse(matr.a,matr.b,matr.c,c.imax,c.imax);
par.phi=zeros(1,c.imax);
par.temp=zeros(1,c.imax);
par.omega=zeros(2,c.imax);
par.ds=zeros(3,c.imax);
par.dp=zeros(1,c.imax);
par.f=zeros(1,c.imax);
par.alpha=zeros(1,c.imax);

par.ds(3,:)=0.;

matr.a = [[1:c.imax],[2:c.imax],[1:c.imax-1]];
matr.b = [[1:c.imax],[1:c.imax-1],[2:c.imax]];
matr.c(1) = 1.;
matr.c(2*c.imax) = 0.;

xxx=1;
if (my_substr(c.prop.c,1,1) == 'C')
  if (str2num(my_substr(c.prop.c,3)) == 0)
    xxx=0;
  end
end


if (str2num(my_split(c.steady,' ',1)) == Inf)
    conc=zeros(8,c.imax);
    par.sigma=zeros(1,c.imax);
  if (c.lim(1)==0)
    [par,c,conc]=solver_nit(r,c,par,v,matr,conc,'1',1);
  else
      [par,c,conc]=solver_it(r,c,par,v,matr,conc,'1',1);
  end
  par.alpha=interp_f(r.alpha,v,c,par.alpha,c.prop.a,par);

  if (c.lim(2) ~= 0)
    par.alpha=1+(par.alpha-1).*conc(1,:)./(conc(1,:)+c.lim(2)); 
  end

  if (c.ref ~= 0)
    [par,c,conc]=solver_it(r,c,par,v,matr,conc,'( par.alpha([2:c.imax-1]).*conc(2,[2:c.imax-1])./( (conc(1,[2:c.imax-1])+(par.alpha([2:c.imax-1])-1.).*conc(2,[2:c.imax-1])) +( (conc(1,[2:c.imax-1])+(par.alpha([2:c.imax-1])-1.).*conc(2,[2:c.imax-1])) ==0))  )',2);
  end

  if (xxx == 1)
    par.ds(2,:)=interp_f(r.diff_prod,v,c,par.ds(2,:),c.prop.dp,par);
    if (c.fia ~= 0)
      par.sigma=coth(par.omega(1,:).*c.dz./2./par.ds(2,:))-1./(par.omega(1,:).*c.dz./2./par.ds(2,:));
    elseif (sum(par.omega(1,:).*c.dz./2./par.ds(2,:)>1) > 0)
      fprintf(2,'\n Peclet number above 1. You might want to consider switching Fiadero scheme on');
      fprintf(2,'\n');
      error('REMAP solver warning');
    end

    if (c.prec == 0)
      [par,c,conc]=solver_nit(r,c,par,v,matr,conc,'-1',3);
    else
      [par,c,conc]=solver_it(r,c,par,v,matr,conc,'c.prec-1',3);
    end

    if (c.ref ~= 0)
      if (c.prec == 0)
	[par,c,conc]=solver_nit(r,c,par,v,matr,conc,'-( par.alpha([2:c.imax-1]).*conc(2,[2:c.imax-1])./( (conc(1,[2:c.imax-1])+(par.alpha([2:c.imax-1])-1.).*conc(2,[2:c.imax-1])) +( (conc(1,[2:c.imax-1])+(par.alpha([2:c.imax-1])-1.).*conc(2,[2:c.imax-1])) ==0))  )',4);
      else
	[par,c,conc]=solver_it(r,c,par,v,matr,conc,'conc(4,[2:c.imax-1])./(conc(3,[2:c.imax-1])+(conc(3,[2:c.imax-1])==0)).*c.prec-( par.alpha([2:c.imax-1]).*conc(2,[2:c.imax-1])./( (conc(1,[2:c.imax-1])+(par.alpha([2:c.imax-1])-1.).*conc(2,[2:c.imax-1])) +( (conc(1,[2:c.imax-1])+(par.alpha([2:c.imax-1])-1.).*conc(2,[2:c.imax-1])) ==0))  )',4);
      end
    end

    if (c.prec ~= 0)
      par.sigma(:)=1;
      par.omega(2,:)=interp_f(r.sed,v,c,par.omega(2,:),c.prop.s,par);
      [par,c,conc]=solver_nit(r,c,par,v,matr,conc,'-c.prec',5);
      if (c.ref ~= 0)
	[par,c,conc]=solver_nit(r,c,par,v,matr,conc,'-c.prec.*conc(4,[2:c.imax-1])./(conc(3,[2:c.imax-1])+(conc(3,[2:c.imax-1])==0))',6);
      end
    end
  end
 
else
  conc=zeros(18,c.imax);
  c.dz=c.z/(c.imax-1);
  timemax=str2num(my_split(c.steady,' ',1));
  par.sigma=zeros(3,c.imax);
  in_s=my_split(c.steady,' ',2),'rt';
 
  

  
  try
    fz=fopen([pwd,'/',in_s],'rt');
    fprintf(2,'Reading from %s\n',in_s);
    fgets(fz);
  catch
    fprintf(2,'\n No such file %s\n',fn);
    fprintf(2,'\n');
    error('REMAP file error');
  end
  i=1;

  num_cols=10;
  [my_in,count]=fscanf(fz,'%g,%g,%g,%g,%g,%g,%g,%g,%g,%g');

  my_in = reshape(my_in,num_cols,count/num_cols);

  conc(1,:)=my_in(2,:);
  conc(3,:)=my_in(3,:);
  conc(5,:)=my_in(4,:);
  conc(2,:)=my_in(8,:);
  conc(4,:)=my_in(9,:);
  conc(6,:)=my_in(10,:);

 
  par.phi=interp_f(r.phi,v,c,par.phi,c.prop.p,par);
  par.temp=interp_f(r.temp,v,c,par.temp,c.prop.t,par);
  par.omega(1,:)=interp_f(r.omega,v,c,par.omega(1,:),c.prop.o,par);
  par.ds(1,:)=interp_f(r.diff_sub,v,c,par.ds(1,:),c.prop.ds,par);
  par.ds(2,:)=interp_f(r.diff_prod,v,c,par.ds(2,:),c.prop.dp,par);
  par.f=interp_f(r.con,v,c,par.f,c.prop.c,par);
  par.alpha=interp_f(r.alpha,v,c,par.alpha,c.prop.a,par);
  par.omega(2,:)=interp_f(r.sed,v,c,par.omega(2,:),c.prop.s,par);
  par.sigma(3,:)=1;

  if (c.fia ~= 0)
    par.sigma(1,:)=coth(par.omega(1,:).*c.dz./2./par.ds(1,:))-1./(par.omega(1,:).*c.dz./2./par.ds(1,:));
    par.sigma(2,:)=coth(par.omega(1,:).*c.dz./2./par.ds(2,:))-1./(par.omega(1,:).*c.dz./2./par.ds(1,:));
  elseif (sum(par.omega(1,:).*c.dz./2./par.ds(1,:)>1) > 0) || (sum(par.omega(1,:).*c.dz./2./par.ds(2,:)>1) > 0)
    fprintf(2,'Peclet number above 1. You might want to consider switching Fiadero scheme on');
    fprintf(2,'\n');
    error('REMAP solver warning');
  end

  time = 0;
  while (time < timemax)
    [par,c,conc]=solver_d(r,c,par,v,matr,conc,'1',1);
    if (c.ref ~= 0)
      [par,c,conc]=solver_d(r,c,par,v,matr,conc,'( par.alpha([2:c.imax-1]).*conc(2,[2:c.imax-1])./( (conc(1,[2:c.imax-1])+(par.alpha([2:c.imax-1])-1.).*conc(2,[2:c.imax-1])) +( (conc(1,[2:c.imax-1])+(par.alpha([2:c.imax-1])-1.).*conc(2,[2:c.imax-1])) ==0))  )',2);
    end

    if (xxx ~= 0)
      [par,c,conc]=solver_d(r,c,par,v,matr,conc,'c.prec-1',3);
      if (c.ref ~= 0) 
	if (c.prec == 0)
	  [par,c,conc]=solver_d(r,c,par,v,matr,conc,'-( par.alpha([2:c.imax-1]).*conc(2,[2:c.imax-1])./( (conc(1,[2:c.imax-1])+(par.alpha([2:c.imax-1])-1.).*conc(2,[2:c.imax-1])) +( (conc(1,[2:c.imax-1])+(par.alpha([2:c.imax-1])-1.).*conc(2,[2:c.imax-1])) ==0))  )',4);
	else
	  [par,c,conc]=solver_d(r,c,par,v,matr,conc,'conc(4,[2:c.imax-1])./(conc(3,[2:c.imax-1])+(conc(3,[2:c.imax-1])==0)).*c.prec-( par.alpha([2:c.imax-1]).*conc(2,[2:c.imax-1])./( (conc(1,[2:c.imax-1])+(par.alpha([2:c.imax-1])-1.).*conc(2,[2:c.imax-1])) +( (conc(1,[2:c.imax-1])+(par.alpha([2:c.imax-1])-1.).*conc(2,[2:c.imax-1])) ==0))  )',4);
	end
      end
      if (c.prec ~= 0)
	par.sigma(:)=1;
	[par,c,conc]=solver_d(r,c,par,v,matr,conc,'-c.prec',5);
	if (c.ref ~= 0)
	  [par,c,conc]=solver_d(r,c,par,v,matr,conc,'-c.prec.*conc(4,[2:c.imax-1])./(conc(3,[2:c.imax-1])+(conc(3,[2:c.imax-1])==0))',6);
	end
      end
    end
	
    time=time+c.dt;

    for i=1:length(strfind(c.steady,' ',2))-1
	tempstr=my_split(c.steady,' ',i+2);
        tempstr=strrep(tempstr,'alpha','par.alpha');
        tempstr=strrep(tempstr,'omega','par.omega');
        ## vectorize is depreciated 
        ## tempstr=vectorize(tempstr);
	eval(tempstr);
    end
    fprintf(2,'%g %g\n',time,c.dt);
  end
end

fprintf(2,'\n Data read from %s\n\n',fn);

endfunction

