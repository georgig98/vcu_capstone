! Programmed and owned by Hubert E. Coburn II (11-30-2018)

!========================================================================================
! The following program allocates a given energy to the energy array for a given channel
! for the 2018-2019 senior design project entitled "Optimization of an Autonomous
! Radiation Detection Platform and Measurement Algorithm"
!========================================================================================

subroutine energyallocate
use vars
implicit none

! Establish variables determined through testing on detector performed by Michael 
! Cartwright in his research 
c1 = 1329.63                           ! First channel
c2 = 2603.69                           ! Second channel
e1 = 660.78                            ! Energy of first channel (keV
e2 = 1333.83                           ! Energy of second Channel (keV)

! Establish energies of each channel up to 4096
do i = 1,nc
    c = i
    energy(i) = (((e2-e1)/(c2-c1))*(c-c1))+e1
end do


end subroutine energyallocate