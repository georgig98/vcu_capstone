! Programmed and owned by Hubert E. Coburn II (12-3-2018)

!========================================================================================
! The following program provides the means of cutting channel number down to 1024 from 
! 4096 for the 2018-2019 senior design project entitled "Optimization of an Autonomous
! Radiation Detection Platform and Measurement Algorithm"
!========================================================================================

subroutine modifydata
use vars
implicit none

! Divide the number of channels (nc) to ge the number of desired channels (ndc)
ndc = nc/4

! Allocate the modified data storage arrays
allocate(energymod(ndc),channelmod(ndc))

! Set x and y equal to their respective states for splitting of data
x = 1
y = 4

do i = 1, ndc
    ! Set subgroups to zero
    cnt = 0
    nrg = 0
    
    ! Break up the data into subgroups
    do j = x, y
        cnt = cnt + channel(j)
		nrg = nrg + energy(j)
    end do
	
	x = x + 4
	y = y + 4
    
    ! Store Subgroups
    channelmod(i) = cnt
    energymod(i) = (nrg/4.0)
end do

end subroutine modifydata