! Programmed and owned by Hubert E. Coburn II (2-27-2019)

!========================================================================================
! The following program arranges and confirms arrays to make sure no errors will
!  show up farther down the line for the 2018-2019 senior design project entitled 
! "Optimization of an Autonomous Radiation Detection Platform and Measurement Algorithm"
!========================================================================================

subroutine arrays
use vars
implicit none

! Determine the expected radiation counts for the amount of time spent collecting
do i = 1,nlines
	expected(i) = slope(i)*tsmax
end do

do i = 1, nlines
    if (expected(i) == 0) then
        ratio(i) = rawdata(i)
    else 
        ratio(i) = rawdata(i)/expected(i)
    end if
end do

! Modify the ratio inequality if need be to maintain good peak following

do i = 1, nlines
    if (ratio(i) > 15) then
        peaks(i) = 1
    else 
        peaks(i) = 0
    end if
end do


end subroutine arrays