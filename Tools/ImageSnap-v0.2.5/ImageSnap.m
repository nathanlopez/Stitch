//
//  ImageSnap.m
//  ImageSnap
//
//  Created by Robert Harder on 9/10/09.
//

#import "ImageSnap.h"


@interface ImageSnap()


- (void)captureOutput:(QTCaptureOutput *)captureOutput 
  didOutputVideoFrame:(CVImageBufferRef)videoFrame 
     withSampleBuffer:(QTSampleBuffer *)sampleBuffer 
       fromConnection:(QTCaptureConnection *)connection;

@end


@implementation ImageSnap



- (id)init{
	self = [super init];
    mCaptureSession = nil;
    mCaptureDeviceInput = nil;
    mCaptureDecompressedVideoOutput = nil;
	mCurrentImageBuffer = nil;
	return self;
}

- (void)dealloc{
	
	if( mCaptureSession )					[mCaptureSession release];
	if( mCaptureDeviceInput )				[mCaptureDeviceInput release];
	if( mCaptureDecompressedVideoOutput )	[mCaptureDecompressedVideoOutput release];
    CVBufferRelease(mCurrentImageBuffer);
    
    [super dealloc];
}


// Returns an array of video devices attached to this computer.
+ (NSArray *)videoDevices{
    NSMutableArray *results = [NSMutableArray arrayWithCapacity:3];
    [results addObjectsFromArray:[QTCaptureDevice inputDevicesWithMediaType:QTMediaTypeVideo]];
    [results addObjectsFromArray:[QTCaptureDevice inputDevicesWithMediaType:QTMediaTypeMuxed]];
    return results;
}

// Returns the default video device or nil if none found.
+ (QTCaptureDevice *)defaultVideoDevice{
	QTCaptureDevice *device = nil;
    
	device = [QTCaptureDevice defaultInputDeviceWithMediaType:QTMediaTypeVideo];
	if( device == nil ){
        device = [QTCaptureDevice defaultInputDeviceWithMediaType:QTMediaTypeMuxed];
	}
    return device;
}

// Returns the named capture device or nil if not found.
+(QTCaptureDevice *)deviceNamed:(NSString *)name{
    QTCaptureDevice *result = nil;
    
    NSArray *devices = [ImageSnap videoDevices];
	for( QTCaptureDevice *device in devices ){
        if ( [name isEqualToString:[device description]] ){
            result = device;
        }   // end if: match
    }   // end for: each device
    
    return result;
}   // end


// Saves an image to a file or standard out if path is nil or "-" (hyphen).
+ (BOOL) saveImage:(NSImage *)image toPath: (NSString*)path{
    
    NSString *ext = [path pathExtension];
    NSData *photoData = [ImageSnap dataFrom:image asType:ext];
    
    // If path is a dash, that means write to standard out
    if( path == nil || [@"-" isEqualToString:path] ){
        NSUInteger length = [photoData length];
        NSUInteger i;
        char *start = (char *)[photoData bytes];
        for( i = 0; i < length; ++i ){
            putc( start[i], stdout );
        }   // end for: write out
        return YES;
    } else {
        return [photoData writeToFile:path atomically:NO];
    }

    
    return NO;
}


/**
 * Converts an NSImage into NSData. Defaults to jpeg if
 * format cannot be determined.
 */
+(NSData *)dataFrom:(NSImage *)image asType:(NSString *)format{
    
    NSData *tiffData = [image TIFFRepresentation];
    
    NSBitmapImageFileType imageType = NSJPEGFileType;
    NSDictionary *imageProps = nil;
    
    
    // TIFF. Special case. Can save immediately.
    if( [@"tif"  rangeOfString:format options:NSCaseInsensitiveSearch].location != NSNotFound ||
	    [@"tiff" rangeOfString:format options:NSCaseInsensitiveSearch].location != NSNotFound ){
        return tiffData;
    }
    
    // JPEG
    else if( [@"jpg"  rangeOfString:format options:NSCaseInsensitiveSearch].location != NSNotFound || 
             [@"jpeg" rangeOfString:format options:NSCaseInsensitiveSearch].location != NSNotFound ){
        imageType = NSJPEGFileType;
        imageProps = [NSDictionary dictionaryWithObject:[NSNumber numberWithFloat:0.9] forKey:NSImageCompressionFactor];
        
    }
    
    // PNG
    else if( [@"png" rangeOfString:format options:NSCaseInsensitiveSearch].location != NSNotFound ){
        imageType = NSPNGFileType;
    }
    
    // BMP
    else if( [@"bmp" rangeOfString:format options:NSCaseInsensitiveSearch].location != NSNotFound ){
        imageType = NSBMPFileType;
    }
    
    // GIF
    else if( [@"gif" rangeOfString:format options:NSCaseInsensitiveSearch].location != NSNotFound ){
        imageType = NSGIFFileType;
    }
    
    NSBitmapImageRep *imageRep = [NSBitmapImageRep imageRepWithData:tiffData];
    NSData *photoData = [imageRep representationUsingType:imageType properties:imageProps];

    return photoData;
}   // end dataFrom



/**
 * Primary one-stop-shopping message for capturing an image.
 * Activates the video source, saves a frame, stops the source,
 * and saves the file.
 */

+(BOOL)saveSingleSnapshotFrom:(QTCaptureDevice *)device toFile:(NSString *)path{
    return [self saveSingleSnapshotFrom:device toFile:path withWarmup:nil];
}

+(BOOL)saveSingleSnapshotFrom:(QTCaptureDevice *)device toFile:(NSString *)path withWarmup:(NSNumber *)warmup{
    return [self saveSingleSnapshotFrom:device toFile:path withWarmup:warmup withTimelapse:nil];
}
     
+(BOOL)saveSingleSnapshotFrom:(QTCaptureDevice *)device 
                       toFile:(NSString *)path 
                   withWarmup:(NSNumber *)warmup 
                withTimelapse:(NSNumber *)timelapse{
    ImageSnap *snap;
    NSImage *image = nil;
    double interval = timelapse == nil ? -1 : [timelapse doubleValue];
    
    snap = [[ImageSnap alloc] init];            // Instance of this ImageSnap class
    verbose("Starting device...");
    if( [snap startSession:device] ){           // Try starting session
        verbose("Device started.\n");
        
        if( warmup == nil ){
            // Skip warmup
            verbose("Skipping warmup period.\n");
        } else {
            double delay = [warmup doubleValue];
            verbose("Delaying %.2lf seconds for warmup...",delay);
            NSDate *now = [[NSDate alloc] init];
            [[NSRunLoop currentRunLoop] runUntilDate:[now dateByAddingTimeInterval: [warmup doubleValue]]];
            [now release];
            verbose("Warmup complete.\n");
        }
        
        if ( interval > 0 ) {
            
            verbose("Time lapse: snapping every %.2lf seconds to current directory.\n", interval);
            
            NSDateFormatter *dateFormatter = [[NSDateFormatter alloc] init];
            [dateFormatter setDateFormat:@"yyyy-MM-dd_HH-mm-ss.SSS"];
            
            // wait a bit to make sure the camera is initialized
            //[[NSRunLoop currentRunLoop] runUntilDate:[NSDate dateWithTimeIntervalSinceNow: 1.0]];
            
            for (unsigned long seq=0; ; seq++)
            {
                NSDate *now = [[NSDate alloc] init];
                NSString *nowstr = [dateFormatter stringFromDate:now];
                
                verbose(" - Snapshot %5lu", seq);
                verbose(" (%s)\n", [nowstr UTF8String]);
                
                // create filename
                NSString *filename = [NSString stringWithFormat:@"snapshot-%05d-%s.jpg", seq, [nowstr UTF8String]];
                
                // capture and write
                image = [snap snapshot];                // Capture a frame
                if (image != nil)  {
                    [ImageSnap saveImage:image toPath:filename];
                    console( "%s\n", [filename UTF8String]);
                } else {
                    error( "Image capture failed.\n" );
                }
                
                // sleep
                [[NSRunLoop currentRunLoop] runUntilDate:[now dateByAddingTimeInterval: interval]];
                
                [now release];
            }

        } else {
            image = [snap snapshot];                // Capture a frame
            
        }
        //NSLog(@"Stopping...");
        [snap stopSession];                     // Stop session
        //NSLog(@"Stopped.");
    }   // end if: able to start session
    
    [snap release];
    
    if ( interval > 0 ){
        return YES;
    } else {
        return image == nil ? NO : [ImageSnap saveImage:image toPath:path];
    }
}   // end


/**
 * Returns current snapshot or nil if there is a problem
 * or session is not started.
 */
-(NSImage *)snapshot{
    verbose( "Taking snapshot...\n");
	
    CVImageBufferRef frame = nil;               // Hold frame we find
    while( frame == nil ){                      // While waiting for a frame
		
		//verbose( "\tEntering synchronized block to see if frame is captured yet...");
        @synchronized(self){                    // Lock since capture is on another thread
            frame = mCurrentImageBuffer;        // Hold current frame
            CVBufferRetain(frame);              // Retain it (OK if nil)
        }   // end sync: self
		//verbose( "Done.\n" );
		
        if( frame == nil ){                     // Still no frame? Wait a little while.
            [[NSRunLoop currentRunLoop] runUntilDate:[NSDate dateWithTimeIntervalSinceNow: 0.1]];
        }   // end if: still nothing, wait
		
    }   // end while: no frame yet
    
    // Convert frame to an NSImage
    NSCIImageRep *imageRep = [NSCIImageRep imageRepWithCIImage:[CIImage imageWithCVImageBuffer:frame]];
    NSImage *image = [[[NSImage alloc] initWithSize:[imageRep size]] autorelease];
    [image addRepresentation:imageRep];
	verbose( "Snapshot taken.\n" );
    
    return image;
}




/**
 * Blocks until session is stopped.
 */
-(void)stopSession{
	verbose("Stopping session...\n" );
    
    // Make sure we've stopped
    while( mCaptureSession != nil ){
		verbose("\tCaptureSession != nil\n");

		verbose("\tStopping CaptureSession...");
        [mCaptureSession stopRunning];
		verbose("Done.\n");

        if( [mCaptureSession isRunning] ){
			verbose( "[mCaptureSession isRunning]");
            [[NSRunLoop currentRunLoop] runUntilDate:[NSDate dateWithTimeIntervalSinceNow: 0.1]];
        }else {
            verbose( "\tShutting down 'stopSession(..)'" );
            if( mCaptureSession )					[mCaptureSession release];
            if( mCaptureDeviceInput )				[mCaptureDeviceInput release];
            if( mCaptureDecompressedVideoOutput )	[mCaptureDecompressedVideoOutput release];
            
            mCaptureSession = nil;
            mCaptureDeviceInput = nil;
            mCaptureDecompressedVideoOutput = nil;
        }   // end if: stopped
        
    }   // end while: not stopped
}


/**
 * Begins the capture session. Frames begin coming in.
 */
-(BOOL)startSession:(QTCaptureDevice *)device{
	
	verbose( "Starting capture session...\n" );
	
    if( device == nil ) {
		verbose( "\tCannot start session: no device provided.\n" );
		return NO;
	}
    
    NSError *error = nil;
    
    // If we've already started with this device, return
    if( [device isEqual:[mCaptureDeviceInput device]] &&
         mCaptureSession != nil &&
        [mCaptureSession isRunning] ){
        return YES;
    }   // end if: already running
	
    else if( mCaptureSession != nil ){
		verbose( "\tStopping previous session.\n" );
        [self stopSession];
    }   // end if: else stop session
    
	
	// Create the capture session
	verbose( "\tCreating QTCaptureSession..." );
    mCaptureSession = [[QTCaptureSession alloc] init];
	verbose( "Done.\n");
	if( ![device open:&error] ){
		error( "\tCould not create capture session.\n" );
        [mCaptureSession release];
        mCaptureSession = nil;
		return NO;
	}
    
	
	// Create input object from the device
	verbose( "\tCreating QTCaptureDeviceInput with %s...", [[device description] UTF8String] );
	mCaptureDeviceInput = [[QTCaptureDeviceInput alloc] initWithDevice:device];
	verbose( "Done.\n");
	if (![mCaptureSession addInput:mCaptureDeviceInput error:&error]) {
		error( "\tCould not convert device to input device.\n");
        [mCaptureSession release];
        [mCaptureDeviceInput release];
        mCaptureSession = nil;
        mCaptureDeviceInput = nil;
		return NO;
	}
    
	
	// Decompressed video output
	verbose( "\tCreating QTCaptureDecompressedVideoOutput...");
	mCaptureDecompressedVideoOutput = [[QTCaptureDecompressedVideoOutput alloc] init];
	[mCaptureDecompressedVideoOutput setDelegate:self];
	verbose( "Done.\n" );
	if (![mCaptureSession addOutput:mCaptureDecompressedVideoOutput error:&error]) {
		error( "\tCould not create decompressed output.\n");
        [mCaptureSession release];
        [mCaptureDeviceInput release];
        [mCaptureDecompressedVideoOutput release];
        mCaptureSession = nil;
        mCaptureDeviceInput = nil;
        mCaptureDecompressedVideoOutput = nil;
		return NO;
	}

    // Clear old image?
	verbose("\tEntering synchronized block to clear memory...");
    @synchronized(self){
        if( mCurrentImageBuffer != nil ){
            CVBufferRelease(mCurrentImageBuffer);
            mCurrentImageBuffer = nil;
        }   // end if: clear old image
    }   // end sync: self
	verbose( "Done.\n");
    
	[mCaptureSession startRunning];
	verbose("Session started.\n");
    
    return YES;
}   // end startSession



// This delegate method is called whenever the QTCaptureDecompressedVideoOutput receives a frame
- (void)captureOutput:(QTCaptureOutput *)captureOutput 
  didOutputVideoFrame:(CVImageBufferRef)videoFrame 
     withSampleBuffer:(QTSampleBuffer *)sampleBuffer 
       fromConnection:(QTCaptureConnection *)connection
{
	verbose( "." );
    if (videoFrame == nil ) {
		verbose( "'nil' Frame captured.\n" );
        return;
    }
    
    // Swap out old frame for new one
    CVImageBufferRef imageBufferToRelease;
    CVBufferRetain(videoFrame);
	
    @synchronized(self){
        imageBufferToRelease = mCurrentImageBuffer;
        mCurrentImageBuffer = videoFrame;
    }   // end sync
    CVBufferRelease(imageBufferToRelease);
    
}

@end


// //////////////////////////////////////////////////////////
//
// ////////  B E G I N   C - L E V E L   M A I N  //////// //
//
// //////////////////////////////////////////////////////////

int processArguments(int argc, const char * argv[]);
void printUsage(int argc, const char * argv[]);
int listDevices();
NSString *generateFilename();
QTCaptureDevice *getDefaultDevice();


// Main entry point. Since we're using Cocoa and all kinds of fancy
// classes, we have to set up appropriate pools and loops.
// Thanks to the example http://lists.apple.com/archives/cocoa-dev/2003/Apr/msg01638.html
// for reminding me how to do it.
int main (int argc, const char * argv[]) {
    NSApplicationLoad();    // May be necessary for 10.5 not to crash.
    
	NSAutoreleasePool *pool;
	pool = [[NSAutoreleasePool alloc] init];
    [NSApplication sharedApplication];
	
    int result = processArguments(argc, argv);
    
    //	[pool release];
    [pool drain];
    return result;
}



/**
 * Process command line arguments and execute program.
 */
int processArguments(int argc, const char * argv[] ){
	
	NSString *filename = nil;
	QTCaptureDevice *device = nil;
    NSNumber *warmup = nil;
    NSNumber *timelapse = nil;

	
	int i;
	for( i = 1; i < argc; ++i ){
		
		// Handle command line switches
		if (argv[i][0] == '-') {
            
            // Dash only? Means write image to stdout
            if( argv[i][1] == 0 ){
                filename = @"-";
                g_quiet = YES;
            } else {
                
                // Which switch was given
                switch (argv[i][1]) {
                    
                    // Help
                    case '?':
                    case 'h':
                        printUsage( argc, argv );
                        return 0;
                        break;

                        
                    // Verbose
                    case 'v':
                        g_verbose = YES;
                        break;
                    
                    case 'q':
                        g_quiet = YES;
                        break;

                        
                    // List devices
                    case 'l': 
                        listDevices();
                        return 0;
                        break;
                        
                    // Specify device
                    case 'd':
                        if( i+1 < argc ){
                            device = [ImageSnap deviceNamed:[NSString stringWithUTF8String:argv[i+1]]];
                            if( device == nil ){
                                error( "Device \"%s\" not found.\n", argv[i+1] );
                                return 11;
                            }   // end if: not found
                            ++i; // Account for "follow on" argument
                        } else {
                            error( "Not enough arguments given with 'd' flag.\n" );
                            return (int)'d';
                        }
                        break;
                        
                    // Specify a warmup period before picture snaps
                    case 'w':
                        if( i+1 < argc ){
                            warmup = [NSNumber numberWithFloat:[[NSString stringWithUTF8String:argv[i+1]] floatValue]];
                            ++i; // Account for "follow on" argument
                        } else {
                            error( "Not enough arguments given with 'w' flag.\n" );
                            return (int)'w';
                        }
                        break;
                        
                    // Timelapse
                    case 't':
                        if( i+1 < argc ){
                            timelapse = [NSNumber numberWithDouble:[[NSString stringWithUTF8String:argv[i+1]] doubleValue]];
                            //g_timelapse = [timelapse doubleValue];
                            ++i; // Account for "follow on" argument
                        } else {
                            error( "Not enough arguments given with 't' flag.\n" );
                            return (int)'t';
                        }
                        break;

                    
                        
                }	// end switch: flag value
            }   // end else: not dash only
		}	// end if: '-'
        
        // Else assume it's a filename
		else {
			filename = [NSString stringWithUTF8String:argv[i]];
		}

	}	// end for: each command line argument
	
    
    // Make sure we have a filename
	if( filename == nil ){
		filename = generateFilename();
		verbose( "No filename specified. Using %s\n", [filename UTF8String] );
	}	// end if: no filename given
	
    if( filename == nil ){
        error( "No suitable filename could be determined.\n" );
        return 1;
    }
	
    
    // Make sure we have a device
	if( device == nil ){
		device = getDefaultDevice();
		verbose( "No device specified. Using %s\n", [[device description] UTF8String] );
	}	// end if: no device given
	
    if( device == nil ){
        error( "No video devices found.\n" );
        return 2;
    } else {
        console( "Capturing image from device \"%s\"...", [[device description] UTF8String] );
    }
	
    
    // Image capture
    if( [ImageSnap saveSingleSnapshotFrom:device toFile:filename withWarmup:warmup withTimelapse:timelapse] ){
        console( "%s\n", [filename UTF8String] );
    } else {
        error( "Error.\n" );
    }   // end else
    
    return 0;
}



void printUsage(int argc, const char * argv[]){
    printf( "USAGE: %s [options] [filename]\n", argv[0] );
    printf( "Version: %s\n", [VERSION UTF8String] );
    printf( "Captures an image from a video device and saves it in a file.\n" );
    printf( "If no device is specified, the system default will be used.\n" );
    printf( "If no filename is specfied, snapshot.jpg will be used.\n" );
    printf( "Supported image types: JPEG, TIFF, PNG, GIF, BMP\n" );
    printf( "  -h          This help message\n" );
    printf( "  -v          Verbose mode\n");
    printf( "  -l          List available video devices\n" );
    printf( "  -t x.xx     Take a picture every x.xx seconds\n" );
    printf( "  -q          Quiet mode. Do not output any text\n");
    printf( "  -w x.xx     Warmup. Delay snapshot x.xx seconds after turning on camera\n" );
    printf( "  -d device   Use named video device\n" );
}





/**
 * Prints a list of video capture devices to standard out.
 */
int listDevices(){
	NSArray *devices = [ImageSnap videoDevices];
    
    [devices count] > 0 
		? printf("Video Devices:\n") 
		: printf("No video devices found.\n");
    
	for( QTCaptureDevice *device in devices ){
		printf( "%s\n", [[device description] UTF8String] );
	}	// end for: each device
    return [devices count];
}

/**
 * Generates a filename for saving the image, presumably
 * because the user didn't specify a filename.
 * Currently returns snapshot.tiff.
 */
NSString *generateFilename(){
	NSString *result = @"snapshot.jpg";
	return result;
}	// end


/**
 * Gets a default video device, or nil if none is found.
 * For now, simply queries ImageSnap. May be fancier
 * in the future.
 */
QTCaptureDevice *getDefaultDevice(){
	return [ImageSnap defaultVideoDevice];
}	// end



