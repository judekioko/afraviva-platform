import {AbsoluteFill, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {loadFont} from '@remotion/google-fonts/Poppins';
import {EndCard, promoDefaultProps} from './Promo';

const {fontFamily} = loadFont('normal', {weights: ['400', '600'], subsets: ['latin']});

export const clipBrandedSchema = z.object({
  // Path inside static/ (publicDir). The file is gitignored: it is third-party content.
  clipSrc: z.string(),
  clipDurationSec: z.number(),
  credit: z.string(),
  endCardSec: z.number(),
  tagline: z.string(),
  contact: z.array(z.string()),
});

export type ClipBrandedProps = z.infer<typeof clipBrandedSchema>;

export const CLIP_FPS = 30;
const CLIP_SEC = 17.2;
const END_SEC = 3;

export const clipBrandedDefaultProps: ClipBrandedProps = {
  clipSrc: 'video/clips/southwark-remembrance.mp4',
  clipDurationSec: CLIP_SEC,
  credit: 'Video: Archdiocese of Southwark',
  endCardSec: END_SEC,
  tagline: promoDefaultProps.tagline,
  contact: promoDefaultProps.contact,
};

export const clipBrandedDuration = (p: Pick<ClipBrandedProps, 'clipDurationSec' | 'endCardSec'>) =>
  Math.round((p.clipDurationSec + p.endCardSec) * CLIP_FPS);

// Source is 576x1024 (9:16), scaled to fill 1080x1920. Badge sits in the top-left,
// clear of TikTok's top bar, right-hand buttons and bottom caption area.
export const ClipBranded: React.FC<ClipBrandedProps> = ({clipSrc, clipDurationSec, credit, endCardSec, tagline, contact}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const clipFrames = Math.round(clipDurationSec * fps);
  const endFrames = Math.round(endCardSec * fps);
  const badge = spring({frame: frame - 10, fps, config: {damping: 200}});
  const badgeOut = interpolate(frame, [clipFrames - 8, clipFrames], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const volume = interpolate(frame, [clipFrames - 15, clipFrames], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill style={{background: '#000', fontFamily}}>
      <Sequence from={0} durationInFrames={clipFrames}>
        <OffthreadVideo src={staticFile(clipSrc)} volume={volume} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        <div style={{position: 'absolute', left: 56, top: 200, opacity: badge * badgeOut, transform: `translateY(${(1 - badge) * -20}px)`}}>
          <Img
            src={staticFile('img/afraviva-media-logo-3.png')}
            style={{width: 320, borderRadius: 12, boxShadow: '0 6px 30px rgba(0,0,0,0.5)', display: 'block'}}
          />
          <div style={{color: '#FBF9F2', fontSize: 24, marginTop: 10, textShadow: '0 2px 8px rgba(0,0,0,0.8)'}}>{credit}</div>
        </div>
      </Sequence>
      <Sequence from={clipFrames} durationInFrames={endFrames}>
        <EndCard contact={contact} tagline={tagline} durationInFrames={endFrames} />
      </Sequence>
    </AbsoluteFill>
  );
};
