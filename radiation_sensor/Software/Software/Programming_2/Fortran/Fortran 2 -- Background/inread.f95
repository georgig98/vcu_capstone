! Programmed and owned by Hubert E. Coburn II (2-6-2019)

!========================================================================================
! The following routine provides the means of reading data from an input file
! for the 2018-2019 senior design project entitled "Optimization of an Autonomous
! Radiation Detection Platform and Measurement Algorithm"
!========================================================================================

subroutine inread
use vars
implicit none

! Open all files that are to be read to determine the slope and intercepts

open(unit=input,file=infile, status='old',action='read',iostat=ierr)
open(unit=input1,file=infile1,status='old',action='read',iostat=ierr)
open(unit=input2,file=infile2,status='old',action='read',iostat=ierr)
open(unit=input3,file=infile3,status='old',action='read',iostat=ierr)
open(unit=input4,file=infile4,status='old',action='read',iostat=ierr)
open(unit=input5,file=infile5,status='old',action='read',iostat=ierr)


! Set the initial number of lines to zero 
nlines = 0

! Read the input file to determine the number of lines in the  file
do 
	read (input,*,iostat = ierr)
		if (ierr /= 0) then
			exit
		else
			nlines = nlines + 1
		end if
end do

! Allocate the raw data storage arrays and rewind the raw data file
allocate(counts(nlines),ts(nlines))
rewind(unit = input)

! Counts and timestamps must both be read to get to the timestamps
do i = 1,nlines
    read(input,*) counts(i),ts(i)
end do

! Determine how long the detector gathered data
tsmax = ts(nlines)

! Reset the nlines variable and then count lines in the files for slope and intercept
nlines = 0

do 
	read (input1,*,iostat = ierr)
		if (ierr /= 0) then
			exit
		else
			nlines = nlines + 1
		end if
end do

! Allocate the arrays for the high and low counts and reset the file to read in counts
allocate(countsl1(nlines),countsh1(nlines))
allocate(countsl2(nlines),countsh2(nlines))
allocate(countsl3(nlines),countsh3(nlines))
allocate(countsl4(nlines),countsh4(nlines))
allocate(countsl5(nlines),countsh5(nlines))


rewind (unit = input1)

! Read the high and low counts from the files
do i = 1, nlines
    read (input1,*) countsl1(i), countsh1(i)
    read (input2,*) countsl2(i), countsh2(i)
    read (input3,*) countsl3(i), countsh3(i)
    read (input4,*) countsl4(i), countsh4(i)
    read (input5,*) countsl5(i), countsh5(i)
end do


end subroutine inread