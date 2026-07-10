import 'dart:math' as math;
import 'package:flutter/material.dart';

typedef _Particle = (double x, double y, double size, double opacity, double speed);

/// Fond brouillard vivant pour la celebration :
/// volutes violacées qui bougent, particules ambrées flottantes,
/// et dégagement radial depuis le centre quand les halos éclatent.
class CelebrationFog extends StatelessWidget {
  final AnimationController ambientCtrl;
  final Animation<double> clearAnim;

  const CelebrationFog({
    super.key,
    required this.ambientCtrl,
    required this.clearAnim,
  });

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: Listenable.merge([ambientCtrl, clearAnim]),
      builder: (_, __) => CustomPaint(
        painter: _CelebrationFogPainter(ambientCtrl.value, clearAnim.value),
        child: const SizedBox.expand(),
      ),
    );
  }
}

class _CelebrationFogPainter extends CustomPainter {
  final double fog;    // cycle ambiant 0 → 1
  final double clear;  // dégagement au burst 0 → 1

  static final List<_Particle> _particles = _buildParticles();

  const _CelebrationFogPainter(this.fog, this.clear);

  static List<_Particle> _buildParticles() {
    final rng = math.Random(99);
    return List.generate(16, (_) => (
      rng.nextDouble(),               // x fraction
      rng.nextDouble(),               // y phase (position de départ dans le cycle)
      1.2 + rng.nextDouble() * 1.8,  // size 1.2 – 3 px
      0.25 + rng.nextDouble() * 0.35, // opacité
      rng.nextBool() ? 1.0 : 2.0,    // vitesse entière → boucle sans saut au reset
    ));
  }

  @override
  void paint(Canvas canvas, Size size) {
    final w = size.width;
    final h = size.height;
    final center = Offset(w / 2, h / 2);

    // — Fond sombre radial : le centre s'éclaircit au burst —
    final ca = (0.83 * (1.0 - clear * 0.96)).clamp(0.0, 0.83);
    canvas.drawRect(
      Rect.fromLTWH(0, 0, w, h),
      Paint()
        ..shader = RadialGradient(
          center: Alignment.center,
          radius: 0.3 + clear * 1.5, // rayon s'élargit en chassant le noir
          colors: [
            const Color(0xFF0D0B1E).withValues(alpha: ca),
            const Color(0xFF020109).withValues(alpha: 0.97),
          ],
        ).createShader(Rect.fromLTWH(0, 0, w, h)),
    );

    final wispA = (1.0 - clear * 0.85).clamp(0.0, 1.0);

    // Orbites elliptiques continues : sin(a) pour x, ±cos(a) pour y → pas de demi-tour.
    final a = fog * math.pi * 2;

    // — Volute 1 : orbite CCW, centre (22 %, 28 %) —
    _wisp(canvas, center,
      cx: w * 0.22 + math.sin(a) * w * 0.12,
      cy: h * 0.28 + math.cos(a) * h * 0.07,
      rx: w * 0.48, ry: h * 0.20,
      color: const Color(0xFFB8A0FF), alpha: wispA * 0.13);

    // — Volute 2 : orbite CW, centre (72 %, 50 %), décalée 120° —
    final a2 = a + 2.094;
    _wisp(canvas, center,
      cx: w * 0.72 + math.sin(a2) * w * 0.10,
      cy: h * 0.50 - math.cos(a2) * h * 0.09,
      rx: w * 0.44, ry: h * 0.18,
      color: const Color(0xFF8060CC), alpha: wispA * 0.15);

    // — Volute 3 : orbite CCW, centre (45 %, 72 %), décalée 240° —
    final a3 = a + 4.189;
    _wisp(canvas, center,
      cx: w * 0.45 + math.sin(a3) * w * 0.09,
      cy: h * 0.72 + math.cos(a3) * h * 0.06,
      rx: w * 0.58, ry: h * 0.24,
      color: const Color(0xFF7040B8), alpha: wispA * 0.12);

    // — Volute 4 : orbite douce, centre (50 %, 44 %), décalée 60° —
    final a4 = a + 1.047;
    _wisp(canvas, center,
      cx: w * 0.50 + math.sin(a4) * w * 0.05,
      cy: h * 0.44 - math.cos(a4) * h * 0.04,
      rx: w * 0.40, ry: h * 0.30,
      color: Colors.white, alpha: wispA * 0.07);

    // — Volute 5 : 2 orbites/cycle, centre (80 %, 18 %), décalée 180° —
    final a5 = fog * math.pi * 4 + math.pi;
    _wisp(canvas, center,
      cx: w * 0.80 + math.sin(a5) * w * 0.08,
      cy: h * 0.18 - math.cos(a5) * h * 0.07,
      rx: w * 0.30, ry: h * 0.14,
      color: const Color(0xFFD0B8FF), alpha: wispA * 0.10);

    // — Particules flottantes (dérivent vers le haut, disparaissent au burst) —
    final pA = (1.0 - clear * 0.90).clamp(0.0, 1.0);
    if (pA > 0.02) {
      for (final (px, py, pSize, pOpacity, pSpeed) in _particles) {
        // pSpeed entier (1 ou 2) → position identique à fog=0 et fog=1 → boucle sans saut.
        // Le % de Dart sur double retourne toujours un résultat non-négatif pour diviseur > 0.
        final y = ((py - fog * pSpeed) % 1.0) * h;
        canvas.drawCircle(
          Offset(px * w, y),
          pSize,
          Paint()
            ..color = Color.lerp(Colors.amber, Colors.white, pOpacity)!
                .withValues(alpha: pA * pOpacity * 0.65),
        );
      }
    }
  }

  /// Dessine une volute elliptique avec repousse radiale au burst.
  void _wisp(
    Canvas canvas,
    Offset center, {
    required double cx, required double cy,
    required double rx, required double ry,
    required Color color, required double alpha,
  }) {
    if (clear > 0) {
      final dx = cx - center.dx;
      final dy = cy - center.dy;
      final dist = math.sqrt(dx * dx + dy * dy).clamp(1.0, double.infinity);
      final push = clear * 180.0; // 180 px max au burst complet
      cx += (dx / dist) * push;
      cy += (dy / dist) * push;
    }
    final rect = Rect.fromCenter(center: Offset(cx, cy), width: rx * 2, height: ry * 2);
    canvas.drawOval(
      rect,
      Paint()
        ..shader = RadialGradient(
          colors: [
            color.withValues(alpha: alpha),
            color.withValues(alpha: alpha * 0.45),
            Colors.transparent,
          ],
          stops: const [0.0, 0.5, 1.0],
        ).createShader(rect),
    );
  }

  @override
  bool shouldRepaint(_CelebrationFogPainter old) =>
      old.fog != fog || old.clear != clear;
}
