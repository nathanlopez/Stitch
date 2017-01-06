//
//  ImageSnap.h
//  ImageSnap
//
//  Created by Robert Harder on 9/10/09.
//
#import <Cocoa/Cocoa.h>
#import <QTKit/QTKit.h>
#include "ImageSnap.h"

#define error(...) fprintf(stderr, __VA_ARGS__)
#define console(...) (!g_quiet && printf(__VA_ARGS__))
#define verbose(...) (g_verbose && !g_quiet && fprintf(stderr, __VA_ARGS__))

BOOL g_verbose = NO;
BOOL g_quiet = NO;
//double g_timelapse = -1;
NSString *VERSION = @"0.2.5";


@interface ImageSnap : NSObject {
    
    QTCaptureSession                    *mCaptureSession;
    QTCaptureDeviceInput                *mCaptureDeviceInput;
    QTCaptureDecompressedVideoOutput    *mCaptureDecompressedVideoOutput;
    CVImageBufferRef                    mCurrentImageBuffer;
}


/**
 * Returns all attached QTCaptureDevice objects that have video.
 * This includes video-only devices (QTMediaTypeVideo) and
 * audio/video devices (QTMediaTypeMuxed).
 *
 * @return autoreleased array of video devices
 */
+(NSArray *)videoDevices;

/**
 * Returns the default QTCaptureDevice object for video
 * or nil if none is found.
 */
+(QTCaptureDevice *)defaultVideoDevice;

/**
 * Returns the QTCaptureDevice with the given name
 * or nil if the device cannot be found.
 */
+(QTCaptureDevice *)deviceNamed:(NSString *)name;

/**
 * Writes an NSImage to disk, formatting it according
 * to the file extension. If path is "-" (a dash), then
 * an jpeg representation is written to standard out.
 */
+ (BOOL) saveImage:(NSImage *)image toPath: (NSString*)path;

/**
 * Converts an NSImage to raw NSData according to a given
 * format. A simple string search is performed for such
 * characters as jpeg, tiff, png, and so forth.
 */
+(NSData *)dataFrom:(NSImage *)image asType:(NSString *)format;



/**
 * Primary one-stop-shopping message for capturing an image.
 * Activates the video source, saves a frame, stops the source,
 * and saves the file.
 */
+(BOOL)saveSingleSnapshotFrom:(QTCaptureDevice *)device toFile:(NSString *)path;
+(BOOL)saveSingleSnapshotFrom:(QTCaptureDevice *)device toFile:(NSString *)path withWarmup:(NSNumber *)warmup;
+(BOOL)saveSingleSnapshotFrom:(QTCaptureDevice *)device toFile:(NSString *)path withWarmup:(NSNumber *)warmup withTimelapse:(NSNumber *)timelapse;

-(id)init;
-(void)dealloc;


-(BOOL)startSession:(QTCaptureDevice *)device;
-(NSImage *)snapshot;
-(void)stopSession;


@end
