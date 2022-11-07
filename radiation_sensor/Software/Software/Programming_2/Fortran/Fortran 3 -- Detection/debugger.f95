! Programmed and owned by Hubert E. Coburn II (2-27-2019)

!========================================================================================
! The following program helps debug to make sure no errors will
!  show up farther down the line for the 2018-2019 senior design project entitled 
! "Optimization of an Autonomous Radiation Detection Platform and Measurement Algorithm"
!========================================================================================

subroutine debugger
use vars
implicit none

do i = 1,nlines
    write(*,*) 'Expected:',expected(i), '   Raw', rawdata(i),'  Energy Level',energies(i),' Ratio',ratio(i),'   peak', peaks(i)
end do



end subroutine debugger