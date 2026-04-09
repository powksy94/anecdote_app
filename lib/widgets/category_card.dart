import 'package:flutter/material.dart';
import 'dart:math' as math;
import '../models/content_type.dart';
import '../generated/app_localizations.dart';
import 'card_decorations.dart';

class Particle {
  final double angle;
  final double speed;
  final double size;
  final Color color;
  final double rotationSpeed;

  Particle({
    required this.angle,
    required this.speed,
    required this.size,
    required this.color,
    required this.rotationSpeed,
  });
}

class CategoryCard extends StatefulWidget {
  final ContentType type;
  final VoidCallback onNavigate;

  const CategoryCard({
    super.key,
    required this.type,
    required this.onNavigate,
  });

  @override
  State<CategoryCard> createState() => CategoryCardState();
}

class CategoryCardState extends State<CategoryCard>
    with TickerProviderStateMixin {
  late final AnimationController _pulseController;
  late final Animation<double> _pulseAnimation;
  late final AnimationController _burstController;
  final math.Random _random = math.Random();

  bool _isPressed = false;
  bool _isBursting = false;
  List<Particle> _particles = [];

  @override
  void initState() {
    super.initState();

    _pulseController = AnimationController(
      vsync: this,
      duration: Duration(milliseconds: 1800 + _random.nextInt(400)),
    )..repeat(reverse: true);

    _pulseAnimation = Tween<double>(begin: 1.0, end: 1.04).animate(
      CurvedAnimation(parent: _pulseController, curve: Curves.easeInOut),
    );

    _burstController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 500),
    );
  }

  @override
  void dispose() {
    _pulseController.dispose();
    _burstController.dispose();
    super.dispose();
  }

  void _generateParticles() {
    final colors = widget.type.gradient;
    _particles = List.generate(12, (index) {
      final angle =
          (index / 12) * 2 * math.pi + _random.nextDouble() * 0.5;
      return Particle(
        angle: angle,
        speed: 70 + _random.nextDouble() * 90,
        size: 6 + _random.nextDouble() * 12,
        color: Color.lerp(colors[0], colors[1], _random.nextDouble())!,
        rotationSpeed: (_random.nextDouble() - 0.5) * 10,
      );
    });
  }

  void _onTapDown(_) {
    setState(() => _isPressed = true);
    _pulseController.stop();
  }

  void _onTapUp(_) {
    setState(() => _isPressed = false);
    _generateParticles();
    setState(() => _isBursting = true);
    _burstController.forward(from: 0).then((_) {
      widget.onNavigate();
    });
  }

  void _onTapCancel() {
    setState(() => _isPressed = false);
    _pulseController.repeat(reverse: true);
  }

  void onNavigationComplete() {
    setState(() => _isBursting = false);
    _burstController.reset();
    _pulseController.repeat(reverse: true);
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    final gradient = widget.type.gradient;

    return SizedBox(
      child: Stack(
        alignment: Alignment.center,
        clipBehavior: Clip.none,
        children: [
          if (_isBursting)
            AnimatedBuilder(
              animation: _burstController,
              builder: (context, _) {
                return Stack(
                  alignment: Alignment.center,
                  clipBehavior: Clip.none,
                  children: _particles.map((particle) {
                    final t = _burstController.value;
                    final easeOut = Curves.easeOut.transform(t);
                    final distance = particle.speed * easeOut;
                    final dx = math.cos(particle.angle) * distance;
                    final dy = math.sin(particle.angle) * distance;
                    final opacity = (1.0 - t).clamp(0.0, 1.0);
                    final scale = 1.0 - t * 0.5;
                    final rotation = particle.rotationSpeed * t * math.pi;

                    return Positioned(
                      left: 80 + dx - particle.size / 2,
                      top: 80 + dy - particle.size / 2,
                      child: Opacity(
                        opacity: opacity,
                        child: Transform.rotate(
                          angle: rotation,
                          child: Container(
                            width: particle.size * scale,
                            height: particle.size * scale,
                            decoration: BoxDecoration(
                              color: particle.color,
                              borderRadius: BorderRadius.circular(3),
                            ),
                          ),
                        ),
                      ),
                    );
                  }).toList(),
                );
              },
            ),
          GestureDetector(
            onTapDown: _onTapDown,
            onTapUp: _onTapUp,
            onTapCancel: _onTapCancel,
            child: AnimatedBuilder(
              animation: Listenable.merge([_pulseAnimation, _burstController]),
              builder: (context, child) {
                if (_isBursting) {
                  final t = _burstController.value;
                  return Opacity(
                    opacity: (1.0 - t * 1.5).clamp(0.0, 1.0),
                    child: Transform.scale(scale: 1.0 - t * 0.2, child: child),
                  );
                }

                return Transform.scale(
                  alignment: Alignment.center,
                  scaleX: _isPressed ? 1.05 : _pulseAnimation.value,
                  scaleY: _isPressed ? 0.92 : _pulseAnimation.value,
                  child: Container(
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(24),
                      boxShadow: [
                        BoxShadow(
                          color: gradient[0].withValues(alpha: 0.4),
                          blurRadius: 16,
                          spreadRadius: 2,
                          offset: const Offset(0, 4),
                        ),
                      ],
                    ),
                    child: child,
                  ),
                );
              },
              child: ClipRRect(
                borderRadius: BorderRadius.circular(24),
                child: Container(
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                      colors: gradient,
                    ),
                  ),
                  child: Stack(
                    children: [
                      buildCardDecoration(widget.type),
                      Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Container(
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: Colors.white.withValues(alpha: 0.2),
                                borderRadius: BorderRadius.circular(16),
                              ),
                              child: Icon(
                                widget.type.icon,
                                size: 32,
                                color: Colors.white,
                              ),
                            ),
                            const SizedBox(height: 12),
                            Text(
                              widget.type.localizedTitle(loc),
                              textAlign: TextAlign.center,
                              style: const TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                                shadows: [
                                  Shadow(
                                    color: Colors.black26,
                                    blurRadius: 4,
                                    offset: Offset(0, 2),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
