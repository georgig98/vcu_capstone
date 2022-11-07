! Programmed and owned by Hubert E. Coburn II (11-29-2018)

!========================================================================================
! The following routine provides the means of reading data from an input file
! for the 2018-2019 senior design project entitled "Optimization of an Autonomous
! Radiation Detection Platform and Measurement Algorithm"
!========================================================================================

subroutine inread
use vars
implicit none

! Open the input file
open(unit=input,file=infile, status='old',action='read',iostat=ierr)

! Set the initial number of lines to zero 
nlines = 0

! Read the input file to determine the number of lines in the  file
do 
	read (input,12,iostat = ierr)
		if (ierr /= 0) then
			exit
		else
			nlines = nlines + 1
		end if
end do


! Allocate the arrays of the subroutines to follow
allocate(counts(nlines),ts(nlines))

! Rewind the input file to be read again
rewind(unit=input)

! Read the count channels from the input file
do i = 1, nlines
    read(input,*) counts(i),ts(i)
end do



11 format(I4,F7.2)
12 format(x)
13 format(t10,F7.2)

end subroutine inread