! Programmed and owned by Hubert E. Coburn II (2-6-2019)

!========================================================================================
! The following program handles the timestamp of counts
! for the 2018-2019 senior design project entitled "Optimization of an Autonomous
! Radiation Detection Platform and Measurement Algorithm"
!========================================================================================

program main
    implicit none
    
    integer :: ierr
    integer :: i, c
    integer :: nlines
    integer :: maxtime
    integer, allocatable :: time(:)
    integer, allocatable :: counts(:)
    integer, parameter :: input = 101
    
    real :: c1, c2, e1, e2
    real :: energy(4096)
    real, allocatable :: ts(:)
    
    character(len = 10), parameter :: infile = 'rawmod.txt'
    
    
    !!!!!!!!!! PROGRAM FOLLOWS !!!!!!!!!!!
        
        !!!!!!!!!! OPEN AND READ !!!!!!!!!!
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

            12 format(x) 
            
        !!!!!!!!!! Energy Allocate !!!!!!!!!!
            ! Establish variables determined through testing on detector performed by Michael 
            ! Cartwright in his research 
            c1 = 1329.63                           ! First channel
            c2 = 2603.69                           ! Second channel
            e1 = 660.78                            ! Energy of first channel (keV
            e2 = 1333.83                           ! Energy of second Channel (keV)

            ! Establish energies of each channel up to 4096
            do i = 1,4096
                c = i
                energy(i) = (((e2-e1)/(c2-c1))*(c-c1))+e1
            end do
        !!!!!!!!!! Assort !!!!!!!!!!
            maxtime = ts(nlines)/1000
            do i = 1, maxtime
                do i = 1
                
end program main