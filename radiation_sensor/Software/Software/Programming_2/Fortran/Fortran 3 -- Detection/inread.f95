! Programmed and owned by Hubert E. Coburn II (2-6-2019)

!========================================================================================
! The following routine provides the means of reading data from an input file
! for the 2018-2019 senior design project entitled "Optimization of an Autonomous
! Radiation Detection Platform and Measurement Algorithm"
!========================================================================================

subroutine inread
use vars
implicit none

open(unit=input1,file=infile1,status='old',action='read',iostat=ierr)

! Set the initial number of lines to zero 
nlines = 0

! Read the input file to determine the number of lines in the  file
do 
	read (input1,*,iostat = ierr)
		if (ierr /= 0) then
			exit
		else
			nlines = nlines + 1
		end if
end do

! Allocate the raw data storage arrays and rewind the raw data file
allocate(counts(nlines),ts(nlines))
rewind(unit = input1)

! Counts and timestamps must both be read to get to the timestamps
do i = 1,nlines
    read(input1,*) counts(i),ts(i)
end do

! Determine how long the detector gathered data
tsmax = ts(nlines)

! Reset the nlines variable and then count lines in the files for slope and intercept
nlines = 0

open(unit=input2,file=infile2,status='old',action='read',iostat=ierr)
open(unit=input3,file=backfile,status='old',action='read',iostat=ierr)

! Read the sorted mod file to determine the number of lines in the  file
do 
	read (input2,*,iostat = ierr)
		if (ierr /= 0) then
			exit
		else
			nlines = nlines + 1
		end if
end do

! Allocate the arrays for the expected radiation counts, energies of each channel, and 
! the actual radiation counts
 
allocate (rawdata(nlines),expected(nlines),energies(nlines),slope(nlines),std(nlines))
allocate(ratio(nlines), peaks(nlines))

! Rewind the raw data input file
rewind (unit = input2)

! Read the raw input and intercepts file
do i = 1, nlines
    read(input2,11) energies(i),rawdata(i)
	read(input3,*) slope(i), std(i)
end do


11 format(T15,F7.2,T45,I6)

end subroutine inread