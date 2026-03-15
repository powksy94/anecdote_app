import 'package:flutter/material.dart';
import 'dart:math' as math;
import 'content_page.dart';
import '../models/content_type.dart';
import '../generated/app_localizations.dart';

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

class HomePage extends StatefulWidget {
  final void Function(Locale locale)? onLocaleChange;

  const HomePage({super.key, this.onLocaleChange});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> with TickerProviderStateMixin {
  final Map<ContentType, AnimationController> _pulseControllers = {};
  final Map<ContentType, Animation<double>> _pulseAnimations = {};
  final Map<ContentType, AnimationController> _burstControllers = {};
  final Map<ContentType, bool> _isPressed = {};
  final Map<ContentType, bool> _isBursting = {};
  final Map<ContentType, List<Particle>> _particles = {};
  final math.Random _random = math.Random();

  @override
  void initState() {
    super.initState();
    for (final type in ContentType.values) {
      _pulseControllers[type] = AnimationController(
        vsync: this,
        duration: Duration(milliseconds: 1800 + _random.nextInt(400)),
      )..repeat(reverse: true);

      _pulseAnimations[type] = Tween<double>(begin: 1.0, end: 1.04).animate(
        CurvedAnimation(
          parent: _pulseControllers[type]!,
          curve: Curves.easeInOut,
        ),
      );

      _burstControllers[type] = AnimationController(
        vsync: this,
        duration: const Duration(milliseconds: 500),
      );

      _isPressed[type] = false;
      _isBursting[type] = false;
      _particles[type] = [];
    }
  }

  @override
  void dispose() {
    for (final controller in _pulseControllers.values) {
      controller.dispose();
    }
    for (final controller in _burstControllers.values) {
      controller.dispose();
    }
    super.dispose();
  }

  void _generateParticles(ContentType type) {
    final colors = type.gradient;
    _particles[type] = List.generate(12, (index) {
      final angle = (index / 12) * 2 * math.pi + _random.nextDouble() * 0.5;
      return Particle(
        angle: angle,
        speed: 70 + _random.nextDouble() * 90,
        size: 6 + _random.nextDouble() * 12,
        color: Color.lerp(colors[0], colors[1], _random.nextDouble())!,
        rotationSpeed: (_random.nextDouble() - 0.5) * 10,
      );
    });
  }

  void _onTapDown(ContentType type) {
    setState(() => _isPressed[type] = true);
    _pulseControllers[type]!.stop();
  }

  void _onTapUp(ContentType type) {
    setState(() => _isPressed[type] = false);
    _startBurst(type);
  }

  void _onTapCancel(ContentType type) {
    setState(() => _isPressed[type] = false);
    _pulseControllers[type]!.repeat(reverse: true);
  }

  void _startBurst(ContentType type) {
    _generateParticles(type);
    setState(() => _isBursting[type] = true);
    _burstControllers[type]!.forward(from: 0).then((_) {
      _navigateToContent(type);
    });
  }

  void _navigateToContent(ContentType type) {
    Navigator.push(
      context,
      PageRouteBuilder(
        pageBuilder: (context, animation, secondaryAnimation) =>
            ContentPage(contentType: type),
        transitionsBuilder: (context, animation, secondaryAnimation, child) {
          return FadeTransition(
            opacity: animation,
            child: child,
          );
        },
        transitionDuration: const Duration(milliseconds: 250),
      ),
    ).then((_) {
      setState(() => _isBursting[type] = false);
      _burstControllers[type]!.reset();
      _pulseControllers[type]!.repeat(reverse: true);
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final loc = AppLocalizations.of(context)!;

    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            const SizedBox(height: 32),
            Text(
              loc.appTitle,
              style: theme.textTheme.headlineMedium?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              loc.chooseCategory,
              style: theme.textTheme.bodyLarge?.copyWith(
                color: theme.colorScheme.onSurface.withValues(alpha:0.6),
              ),
            ),
            const SizedBox(height: 32),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20),
                child: GridView.builder(
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2,
                    mainAxisSpacing: 16,
                    crossAxisSpacing: 16,
                    childAspectRatio: 1.0,
                  ),
                  itemCount: ContentType.values.length,
                  itemBuilder: (context, index) {
                    final type = ContentType.values[index];
                    return _buildContentBox(type, loc);
                  },
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildContentBox(ContentType type, AppLocalizations loc) {
    final gradient = type.gradient;

    return SizedBox(
      child: Stack(
        alignment: Alignment.center,
        clipBehavior: Clip.none,
        children: [
          if (_isBursting[type]!)
            AnimatedBuilder(
              animation: _burstControllers[type]!,
              builder: (context, _) {
                return Stack(
                  alignment: Alignment.center,
                  clipBehavior: Clip.none,
                  children: _particles[type]!.map((particle) {
                    final t = _burstControllers[type]!.value;
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
            onTapDown: (_) => _onTapDown(type),
            onTapUp: (_) => _onTapUp(type),
            onTapCancel: () => _onTapCancel(type),
            child: AnimatedBuilder(
              animation: Listenable.merge([
                _pulseAnimations[type]!,
                _burstControllers[type]!,
              ]),
              builder: (context, child) {
                if (_isBursting[type]!) {
                  final t = _burstControllers[type]!.value;
                  final scale = 1.0 - t * 0.2;
                  final opacity = (1.0 - t * 1.5).clamp(0.0, 1.0);
                  return Opacity(
                    opacity: opacity,
                    child: Transform.scale(
                      scale: scale,
                      child: child,
                    ),
                  );
                }

                double scaleX;
                double scaleY;

                if (_isPressed[type]!) {
                  scaleX = 1.05;
                  scaleY = 0.92;
                } else {
                  scaleX = _pulseAnimations[type]!.value;
                  scaleY = _pulseAnimations[type]!.value;
                }

                return Transform.scale(
                  alignment: Alignment.center,
                  scaleX: scaleX,
                  scaleY: scaleY,
                  child: Container(
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(24),
                      boxShadow: [
                        BoxShadow(
                          color: gradient[0].withValues(alpha:0.4),
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
                      _buildDecorations(type),
                      Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Container(
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: Colors.white.withValues(alpha:0.2),
                                borderRadius: BorderRadius.circular(16),
                              ),
                              child: Icon(
                                type.icon,
                                size: 32,
                                color: Colors.white,
                              ),
                            ),
                            const SizedBox(height: 12),
                            Text(
                              type.localizedTitle(loc),
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

  Widget _buildDecorations(ContentType type) {
    switch (type) {
      case ContentType.anecdote:
        return Stack(
          children: [
            Positioned(
              top: -20,
              right: -20,
              child: _decorCircle(60, Colors.white.withValues(alpha:0.1)),
            ),
            Positioned(
              bottom: -30,
              left: -30,
              child: _decorCircle(80, Colors.white.withValues(alpha:0.08)),
            ),
            Positioned(
              top: 20,
              left: 10,
              child: Icon(Icons.star, size: 12, color: Colors.white.withValues(alpha:0.3)),
            ),
            Positioned(
              bottom: 40,
              right: 20,
              child: Icon(Icons.star, size: 8, color: Colors.white.withValues(alpha:0.25)),
            ),
          ],
        );
      case ContentType.chuckNorris:
        return Stack(
          children: [
            Positioned(
              top: -15,
              left: -15,
              child: Transform.rotate(
                angle: 0.3,
                child: _decorRect(50, 50, Colors.white.withValues(alpha:0.1)),
              ),
            ),
            Positioned(
              bottom: -20,
              right: -10,
              child: Transform.rotate(
                angle: -0.5,
                child: _decorRect(40, 40, Colors.white.withValues(alpha:0.08)),
              ),
            ),
            Positioned(
              top: 15,
              right: 15,
              child: Icon(Icons.bolt, size: 14, color: Colors.white.withValues(alpha:0.3)),
            ),
          ],
        );
      case ContentType.advice:
        return Stack(
          children: [
            Positioned(
              top: -25,
              right: 20,
              child: _decorCircle(50, Colors.white.withValues(alpha:0.12)),
            ),
            Positioned(
              bottom: -15,
              left: 30,
              child: _decorCircle(35, Colors.white.withValues(alpha:0.1)),
            ),
            Positioned(
              top: 40,
              left: 5,
              child: _decorCircle(15, Colors.white.withValues(alpha:0.15)),
            ),
            Positioned(
              bottom: 30,
              right: 10,
              child: Icon(Icons.format_quote, size: 16, color: Colors.white.withValues(alpha:0.25)),
            ),
          ],
        );
      case ContentType.history:
        return Stack(
          children: [
            Positioned(
              top: 10,
              right: -20,
              child: Transform.rotate(
                angle: 0.2,
                child: _decorRect(60, 20, Colors.white.withValues(alpha:0.1)),
              ),
            ),
            Positioned(
              bottom: 20,
              left: -15,
              child: Transform.rotate(
                angle: -0.15,
                child: _decorRect(50, 15, Colors.white.withValues(alpha:0.08)),
              ),
            ),
            Positioned(
              top: 50,
              left: 15,
              child: Icon(Icons.access_time, size: 12, color: Colors.white.withValues(alpha:0.3)),
            ),
          ],
        );
      case ContentType.animals:
        return Stack(
          children: [
            Positioned(
              top: -10,
              left: 40,
              child: _decorCircle(30, Colors.white.withValues(alpha:0.12)),
            ),
            Positioned(
              bottom: -25,
              right: -25,
              child: _decorCircle(70, Colors.white.withValues(alpha:0.08)),
            ),
            Positioned(
              top: 25,
              right: 10,
              child: Icon(Icons.eco, size: 14, color: Colors.white.withValues(alpha:0.3)),
            ),
            Positioned(
              bottom: 45,
              left: 10,
              child: Icon(Icons.eco, size: 10, color: Colors.white.withValues(alpha:0.2)),
            ),
          ],
        );
    }
  }

  Widget _decorCircle(double size, Color color) {
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: color,
      ),
    );
  }

  Widget _decorRect(double width, double height, Color color) {
    return Container(
      width: width,
      height: height,
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(8),
      ),
    );
  }
}
