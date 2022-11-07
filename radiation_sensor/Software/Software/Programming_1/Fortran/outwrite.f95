! Programmed and owned by Hubert E. Coburn II (11-30-2018)

!========================================================================================
! The following program writes the output of the energies and counts
! for the 2018-2019 senior design project entitled "Optimization of an Autonomous
! Radiation Detection Platform and Measurement Algorithm"
!========================================================================================

subroutine outwrite
use vars
implicit none

! Gen names for the files


! Open the output file
open(unit=output1,file=outfile,action='write')
open(unit=output2,file=outfile2,action='write') 

! Write the energy and then the number of counts up to channel 4094--4094 and 4095 
! have been show to provide faulty data and are therefore excluded
do i = 1,(nc-2)
    if (energy(i)>= 0) then
        write(output1,21) energy(i), channel(i)
    end if
end do

do i = 1,(ndc-1)
    if (energymod(i) >= 0) then    
        write(output2,21) energymod(i), channelmod(i)
    end if 
end do

21 format(x,'Energy(keV):',T15,F7.2,T35,'Counts:',T45,I4)



end subroutine outwrite