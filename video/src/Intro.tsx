import {AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {loadFont} from '@remotion/google-fonts/Poppins';

const {fontFamily} = loadFont('normal', {weights: ['400', '700'], subsets: ['latin']});

export const introSchema = z.object({
  title: z.string(),
  subtitle: z.string(),
});

// Brand colours mirror tailwind.config.js.
const FOREST = '#2C4A3B';
const GOLD = '#B98A46';
const PAPER = '#FBF9F2';

export const Intro: React.FC<z.infer<typeof introSchema>> = ({title, subtitle}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();

  const logoScale = spring({frame, fps, config: {damping: 200}});
  const titleOpacity = interpolate(frame, [20, 45], [0, 1], {extrapolateRight: 'clamp'});
  const subtitleOpacity = interpolate(frame, [45, 70], [0, 1], {extrapolateRight: 'clamp'});
  const fadeOut = interpolate(frame, [durationInFrames - 20, durationInFrames], [1, 0], {
    extrapolateLeft: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: FOREST,
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily,
        opacity: fadeOut,
      }}
    >
      <Img src={staticFile('img/afraviva-media-logo-3.png')} style={{height: 330, borderRadius: 6, transform: `scale(${logoScale})`}} />
      <h1 style={{color: PAPER, fontSize: 120, fontWeight: 700, margin: '40px 0 0', opacity: titleOpacity}}>{title}</h1>
      <p style={{color: GOLD, fontSize: 52, margin: '16px 0 0', opacity: subtitleOpacity}}>{subtitle}</p>
    </AbsoluteFill>
  );
};
