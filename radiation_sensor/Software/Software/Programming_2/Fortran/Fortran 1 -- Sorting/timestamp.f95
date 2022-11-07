! Programmed and owned by Hubert E. Coburn II (2-6-2019)

!========================================================================================
! The following program handles the timestamp of counts
! for the 2018-2019 senior design project entitled "Optimization of an Autonomous
! Radiation Detection Platform and Measurement Algorithm"
!========================================================================================

subroutine timestamp
use vars
implicit none

!

! Set all channel counts equal to zero to avoid code breaking errors
do i = 1,nc
    channeld(i) = 0
    channelu(i) = 0
end do

tsmax = ts(nlines)

! Run through the entire counts group and arrange them into channel bins
do i = 1,nlines
    if (ts(i)<(tsmax/2)) then
        n = counts(i)
        channeld(n) = channeld(n) + 1
    end if
end do

do i = 1,nlines 
    n = counts(i)
    channelu(n) = channelu(n) + 1
end do



allocate(channelmodl(ndc),channelmodu(ndc))

! Set x and y equal to their respective states for splitting of data
x = 1
y = 4

do i = 1, ndc
    ! Set subgroups to zero
    cnt = 0
    nrg = 0
    
    ! Break up the data into subgroups
    do j = x, y
        cnt = cnt + channeld(j)
		nrg = nrg + channelu(j)
    end do
	
	x = x + 4
	y = y + 4
    
    ! Store Subgroups
    channelmodl(i) = cnt
    channelmodu(i) = nrg
end do





end subroutine timestamp