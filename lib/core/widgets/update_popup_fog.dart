import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'update_popup.dart';

/// Affiche la célébration post-mise-à-jour : fond quasi-noir (brouillard)
/// qui s'installe en 500 ms, puis l'ampoule s'allume et les halos solaires
/// explosent plein-écran.
Future<T?> showCelebrationDialog<T>(BuildContext context) {
  return showGeneralDialog<T>(
    context: context,
    barrierDismissible: false,
    // Le fond sombre est géré par CelebrationFog à l'intérieur du widget
    barrierColor: Colors.transparent,
    transitionDuration: Duration.zero,
    pageBuilder: (ctx, _, __) => const Material(
      color: Colors.transparent,
      child: UpdatePopup(mode: UpdatePopupMode.celebration),
    ),
  );
}

/// Affiche le popup de mise à jour avec un vrai brouillard animé qui recouvre
/// toute la home page. Le contenu du popup (ampoule + texte + boutons)
/// flotte au-dessus de ce fond obscurci.
Future<T?> showUpdateFogDialog<T>(
  BuildContext context, {
  VoidCallback? onLater,
}) {
  return showGeneralDialog<T>(
    context: context,
    barrierDismissible: false,
    barrierColor: Colors.transparent,
    transitionDuration: const Duration(milliseconds: 900),
    transitionBuilder: (ctx, anim, _, child) => _FogTransition(
      animation: anim,
      child: child,
    ),
    // Material fix : sans ce wrapper les Text héritent d'un style sans contexte
    // (TextStyle avec soulignement jaune — comportement Flutter par défaut hors Material).
    pageBuilder: (ctx, _, __) => Material(
      color: Colors.transparent,
      child: UpdatePopup(
        mode: UpdatePopupMode.update,
        onLater: onLater,
      ),
    ),
  );
}

/// Transition brouillard : fond sombre + volutes de brume animées en continu.
class _FogTransition extends StatefulWidget {
  final Animation<double> animation;
  final Widget child;

  const _FogTransition({required this.animation, required this.child});

  @override
  State<_FogTransition> createState() => _FogTransitionState();
}

class _FogTransitionState extends State<_FogTransition>
    with SingleTickerProviderStateMixin {
  late final AnimationController _fogCtrl;

  @override
  void initState() {
    super.initState();
    _fogCtrl = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 10),
    )..repeat();
  }

  @override
  void dispose() {
    _fogCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: Listenable.merge([widget.animation, _fogCtrl]),
      builder: (context, _) {
        final t = Curves.easeInOut.transform(widget.animation.value);
        return Stack(
          fit: StackFit.expand,
          children: [
            // Brouillard : fond sombre + volutes violacées
            CustomPaint(painter: _FogPainter(t, _fogCtrl.value)),
            // Popup : ampoule + texte + boutons
            widget.child,
          ],
        );
      },
    );
  }
}

/// Peint un fond sombre et 5 volutes de brume qui se déplacent lentement.
class _FogPainter extends CustomPainter {
  final double t;    // progression route 0 → 1
  final double fog;  // cycle continu des volutes 0 → 1

  const _FogPainter(this.t, this.fog);

  @override
  void paint(Canvas canvas, Size size) {
    if (t <= 0) return;

    final w = size.width;
    final h = size.height;

    // — Fond quasi-opaque radial (assombrissement de la home page) —
    final basePaint = Paint()
      ..shader = RadialGradient(
        center: Alignment.center,
        radius: 1.6,
        colors: [
          const Color(0xFF0D0B1E).withValues(alpha: t * 0.83),
          const Color(0xFF020109).withValues(alpha: t * 0.97),
        ],
      ).createShader(Rect.fromLTWH(0, 0, w, h));
    canvas.drawRect(Rect.fromLTWH(0, 0, w, h), basePaint);

    // Les volutes apparaissent après que le fond est à 25 % de son opacité cible
    if (t < 0.25) return;
    final fa = ((t - 0.25) / 0.75).clamp(0.0, 1.0); // fog alpha factor

    // — Volute 1 : haut gauche, dérive vers la droite —
    _drawWisp(canvas, size,
      cx: w * (0.15 + math.sin(fog * math.pi * 2) * 0.12),
      cy: h * (0.28 + math.cos(fog * math.pi * 2 + 0.5) * 0.06),
      rx: w * 0.48, ry: h * 0.20,
      color: const Color(0xFFB8A0FF), alpha: fa * 0.13,
    );

    // — Volute 2 : centre droite, dérive verticalement —
    _drawWisp(canvas, size,
      cx: w * (0.72 + math.cos((fog + 0.3) * math.pi * 2) * 0.10),
      cy: h * (0.50 + math.sin((fog + 0.3) * math.pi * 2) * 0.09),
      rx: w * 0.44, ry: h * 0.18,
      color: const Color(0xFF8060CC), alpha: fa * 0.15,
    );

    // — Volute 3 : bas centre, lente et large —
    _drawWisp(canvas, size,
      cx: w * (0.45 + math.sin((fog + 0.6) * math.pi * 2) * 0.09),
      cy: h * (0.72 + math.cos((fog + 0.6) * math.pi * 2 + 1.0) * 0.06),
      rx: w * 0.58, ry: h * 0.24,
      color: const Color(0xFF7040B8), alpha: fa * 0.12,
    );

    // — Volute 4 : centre, halo blanc (lumière filtrant à travers le brouillard) —
    _drawWisp(canvas, size,
      cx: w * 0.50,
      cy: h * (0.44 + math.sin((fog + 0.8) * math.pi * 2) * 0.03),
      rx: w * 0.40, ry: h * 0.30,
      color: Colors.white, alpha: fa * 0.07,
    );

    // — Volute 5 : haut droite, petite et plus rapide (cycle × 1.5) —
    _drawWisp(canvas, size,
      cx: w * (0.80 + math.cos((fog * 1.5 + 0.15) * math.pi * 2) * 0.08),
      cy: h * (0.18 + math.sin((fog * 1.5 + 0.15) * math.pi * 2) * 0.07),
      rx: w * 0.30, ry: h * 0.14,
      color: const Color(0xFFD0B8FF), alpha: fa * 0.10,
    );
  }

  void _drawWisp(
    Canvas canvas, Size size, {
    required double cx, required double cy,
    required double rx, required double ry,
    required Color color, required double alpha,
  }) {
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
  bool shouldRepaint(_FogPainter old) => old.t != t || old.fog != fog;
}
