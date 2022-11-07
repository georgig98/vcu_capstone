! Programmed and owned by Hubert E. Coburn II (2-6-2019)

!========================================================================================
! The following subroutine determines the expected radiation formulas over all channels
! for the 2018-2019 senior design project entitled "Optimization of an Autonomous
! Radiation Detection Platform and Measurement Algorithm"
!========================================================================================

subroutine backdata
use vars
implicit none

! formulate the average count for each channel

allocate(slope(nlines), sd(nlines), countshavg(nlines))

do i = 1,nlines
    countshavg(i) = real((countsh1(i)+countsh2(i)+countsh3(i)+countsh4(i)+countsh5(i))/5.0)
end do


! Determine slope of each channel

do i = 1,nlines
    slope(i) = countshavg(i)/tsmax
    sd(i) = (countshavg(i)**(0.5))/tsmax
end do



! Determine the intercept for each channel
 


end subroutine backdata   
   