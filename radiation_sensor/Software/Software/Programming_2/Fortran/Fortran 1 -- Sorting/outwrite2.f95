! Programmed and owned by Hubert E. Coburn II (2-6-2019)

!========================================================================================
! The following program writes the output of the energies and counts
! for the 2018-2019 senior design project entitled "Optimization of an Autonomous
! Radiation Detection Platform and Measurement Algorithm"
!========================================================================================

subroutine outwrite2
use vars
implicit none

! Open the output file
open(unit=output1,file=outfile1,action='write') 

! Write the energy and then the number of counts up to channel 4094--4094 and 4095 
! have been show to provide faulty data and are therefore excluded

do i = 1,(ndc)
    if (energymod(i) >= 0) then 
        write(output1,22) channelmodl(i), channelmodu(i)
    end if
end do


22 format(x,I6,T15,I6)



end subroutine outwrite2