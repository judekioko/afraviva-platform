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
  // On-screen message cards, taken from the original post's caption.
  messages: z.array(z.object({startSec: z.number(), endSec: z.number(), heading: z.string(), text: z.string()})),
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
  messages: [
    {
      startSec: 0.8,
      endSec: 8.6,
      heading: 'Remembrance Sunday',
      text: 'We give thanks to God and pray with sorrow for those who gave their lives in war, and for the repose of their souls.',
    },
    {
      startSec: 8.9,
      endSec: 16.6,
      heading: 'Let us pray',
      text: 'May the Lord Jesus, the Prince of Peace, bring healing to our world.',
    },
  ],
  tagline: promoDefaultProps.tagline,
  contact: promoDefaultProps.contact,
};

export const clipBrandedDuration = (p: Pick<ClipBrandedProps, 'clipDurationSec' | 'endCardSec'>) =>
  Math.round((p.clipDurationSec + p.endCardSec) * CLIP_FPS);

const MessageCard: React.FC<{heading: string; text: string; durationInFrames: number}> = ({heading, text, durationInFrames}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 12, durationInFrames - 12, durationInFrames], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const rise = interpolate(frame, [0, 14], [24, 0], {extrapolateRight: 'clamp'});
  // Sits above the prayer graphic, left of TikTok's button column.
  return (
    <div
      style={{
        position: 'absolute',
        left: 56,
        top: 700,
        width: 840,
        opacity,
        transform: `translateY(${rise}px)`,
        background: 'linear-gradient(180deg, rgba(27,47,38,0.82), rgba(27,47,38,0.7))',
        borderLeft: '8px solid #B98A46',
        borderRadius: 6,
        padding: '26px 34px',
        boxShadow: '0 8px 30px rgba(0,0,0,0.45)',
      }}
    >
      <div style={{color: '#CDAB7A', fontSize: 30, fontWeight: 600, letterSpacing: 1, textTransform: 'uppercase'}}>{heading}</div>
      <div style={{color: '#FBF9F2', fontSize: 42, lineHeight: 1.3, marginTop: 10}}>{text}</div>
    </div>
  );
};

// Source is 576x1024 (9:16), scaled to fill 1080x1920. Badge sits in the top-left,
// clear of TikTok's top bar, right-hand buttons and bottom caption area.
export const ClipBranded: React.FC<ClipBrandedProps> = ({clipSrc, clipDurationSec, credit, endCardSec, messages, tagline, contact}) => {
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
        {messages.map((m) => (
          <Sequence key={m.startSec} from={Math.round(m.startSec * fps)} durationInFrames={Math.round((m.endSec - m.startSec) * fps)}>
            <MessageCard heading={m.heading} text={m.text} durationInFrames={Math.round((m.endSec - m.startSec) * fps)} />
          </Sequence>
        ))}
      </Sequence>
      <Sequence from={clipFrames} durationInFrames={endFrames}>
        <EndCard contact={contact} tagline={tagline} durationInFrames={endFrames} />
      </Sequence>
    </AbsoluteFill>
  );
};
