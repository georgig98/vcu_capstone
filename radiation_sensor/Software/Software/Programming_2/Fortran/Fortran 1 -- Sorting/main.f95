! Programmed and owned by Hubert E. Coburn II (11-29-2018)

!========================================================================================
! The following program provides the means of reading, manipulating, and writing data
! for the 2018-2019 senior design project entitled "Optimization of an Autonomous
! Radiation Detection Platform and Measurement Algorithm"

! Always remember when looking at all loops that the last one or two pieces of data
! are exclued due to error of the radiation detector -- this usually means the one or
! two is subtracted from the variables nc or ndc.
!========================================================================================

program main
use vars
implicit none

! Read the input file
call inread

! Rearrange the data
call arrange

! Allocate the energy array for all channels
call energyallocate

! Modify the data to cut the number of channels down
call modifydata

! Write energies and counts
call outwrite

! Timestamp all the channel counts
call timestamp

! write the timestamped channel counts
call outwrite2

end program main