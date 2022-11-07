! Programmed and owned by Hubert E. Coburn II (11-29-2018)

!========================================================================================
! The following program provides the means of rearranging input data 
! for the 2018-2019 senior design project entitled "Optimization of an Autonomous
! Radiation Detection Platform and Measurement Algorithm"
!========================================================================================

subroutine arrange
use vars
implicit none

! Set all channel counts equal to zero
do i = 1,nc
    channel(i) = 0
end do

! Run through the entire counts group and arrange them into channel bins
do i = 1,nlines
    n = counts(i)
    channel(n) = channel(n) + 1
end do

end subroutine arrange