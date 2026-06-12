# Légende des clés JSON
# n   : name (nom de l'os)
# reg : region (région anatomique)
# cnt : count (nombre dans le corps)
# tp  : type (type d'os : Long / Short / Flat / Irregular / Sesamoid)
# fn  : function (fonction principale)
# ff  : famous for (fait marquant)
# im  : image URL (ajouté par le générateur)

HUMAN_BONES = [
    # ── Crâne ─────────────────────────────────────────────────────────────────
    {"n":"Frontal bone","reg":"Skull","cnt":"1","tp":"Flat",
     "fn":"Forms forehead, roof of eye sockets, and front part of skull",
     "ff":"Contains the frontal sinuses; target of facial surgical reconstruction; named from Latin 'frons' (forehead)"},

    {"n":"Parietal bone","reg":"Skull","cnt":"2","tp":"Flat",
     "fn":"Forms the top and sides of the cranium; protects the parietal lobe",
     "ff":"The two parietals meet at the sagittal suture — the most prominent seam on the top of the skull"},

    {"n":"Temporal bone","reg":"Skull","cnt":"2","tp":"Irregular",
     "fn":"Houses the entire hearing apparatus (cochlea, ear canal); mastoid process; anchors jaw muscles",
     "ff":"Contains more anatomy per volume than any other bone; includes the internal ear, ear canal and mastoid air cells"},

    {"n":"Occipital bone","reg":"Skull","cnt":"1","tp":"Flat",
     "fn":"Forms back and base of skull; foramen magnum allows spinal cord to pass to brain",
     "ff":"The foramen magnum is one of the largest holes in the skull; its position distinguishes human bipedalism from apes"},

    {"n":"Sphenoid bone","reg":"Skull","cnt":"1","tp":"Irregular",
     "fn":"Butterfly-shaped keystone of the skull base; houses pituitary gland in sella turcica",
     "ff":"Articulates with every other cranial bone — called the 'keystone'; the sella turcica (Turkish saddle) cradles the pituitary"},

    {"n":"Ethmoid bone","reg":"Skull","cnt":"1","tp":"Irregular",
     "fn":"Forms nasal cavity roof and septum; cribriform plate transmits olfactory nerves",
     "ff":"The cribriform plate ('sieve-like') has ~20 tiny holes per side for olfactory nerve fibres; damage causes loss of smell"},

    {"n":"Nasal bone","reg":"Skull","cnt":"2","tp":"Flat",
     "fn":"Forms the bridge of the nose; provides attachment for nasal cartilages",
     "ff":"The most frequently broken bone in sports and falls; nasal fractures account for ~40 % of all facial fractures"},

    {"n":"Vomer","reg":"Skull","cnt":"1","tp":"Flat",
     "fn":"Forms the lower posterior part of the nasal septum",
     "ff":"Named from Latin 'vomer' (ploughshare) for its shape; deviation of the vomer causes nasal obstruction in ~80 % of adults"},

    {"n":"Mandible","reg":"Face","cnt":"1","tp":"Irregular",
     "fn":"Lower jaw; holds the lower teeth; allows chewing, speaking and swallowing",
     "ff":"The only movable bone of the skull; the mandible condyle is the only synovial joint in the head"},

    {"n":"Maxilla","reg":"Face","cnt":"2","tp":"Irregular",
     "fn":"Forms upper jaw, hard palate, floor of orbit; holds upper teeth",
     "ff":"Contains the largest sinus in the skull — the maxillary sinus; fused at birth; a cleft palate involves the maxilla"},

    {"n":"Zygomatic bone","reg":"Face","cnt":"2","tp":"Irregular",
     "fn":"Forms the cheekbone and lateral orbital wall; provides facial prominence",
     "ff":"'Cheekbone' fractures are the 2nd most common facial fracture; the zygomatic arch bridges to the temporal bone"},

    {"n":"Lacrimal bone","reg":"Face","cnt":"2","tp":"Flat",
     "fn":"Forms part of the medial orbital wall; contains the lacrimal groove for tear drainage",
     "ff":"Smallest and most fragile facial bone (fingernail-thin); the nasolacrimal duct runs through it to drain tears into the nose"},

    {"n":"Palatine bone","reg":"Face","cnt":"2","tp":"Irregular",
     "fn":"Forms the posterior hard palate, nasal floor and part of the orbital floor",
     "ff":"L-shaped; cleft palate surgery often involves the palatine; also contributes to the pterygopalatine fossa — a nerve crossroads"},

    {"n":"Inferior nasal concha","reg":"Face","cnt":"2","tp":"Irregular",
     "fn":"Scroll-shaped bone projecting into the nasal cavity; creates turbulence to warm and humidify air",
     "ff":"One of only three independent bones in the face (not fused); turbinate reduction surgery treats chronic nasal obstruction"},

    {"n":"Hyoid bone","reg":"Throat","cnt":"1","tp":"Irregular",
     "fn":"Supports and moves the tongue; anchors throat muscles; enables swallowing and speech",
     "ff":"The only bone in the body that does not articulate with any other bone; hyoid fracture is rare but indicates strangulation"},

    # ── Osselets de l'oreille ─────────────────────────────────────────────────
    {"n":"Malleus","reg":"Middle ear","cnt":"2","tp":"Irregular",
     "fn":"Hammer-shaped; attached to eardrum; transmits sound vibrations to the incus",
     "ff":"Largest ear ossicle; its handle fuses with the eardrum; named from Latin 'malleus' (hammer)"},

    {"n":"Incus","reg":"Middle ear","cnt":"2","tp":"Irregular",
     "fn":"Anvil-shaped; transfers vibrations from malleus to stapes",
     "ff":"Named from Latin 'incus' (anvil); least frequently dislocated ossicle despite being in the middle of the chain"},

    {"n":"Stapes","reg":"Middle ear","cnt":"2","tp":"Irregular",
     "fn":"Stirrup-shaped; transmits vibrations from incus to oval window of inner ear",
     "ff":"Smallest bone in the human body (~3 mm); stapedius muscle protects it from loud noises — the smallest muscle too"},

    # ── Colonne vertébrale ────────────────────────────────────────────────────
    {"n":"Atlas (C1)","reg":"Spine","cnt":"1","tp":"Irregular",
     "fn":"Supports the skull; allows nodding ('yes' movement); has no vertebral body",
     "ff":"Named after the Titan Atlas who held up the sky; the only vertebra with no vertebral body — just two arches"},

    {"n":"Axis (C2)","reg":"Spine","cnt":"1","tp":"Irregular",
     "fn":"Provides pivot for head rotation ('no' movement) via the odontoid process (dens)",
     "ff":"The dens is a peg-shaped process that projects into the atlas ring; fracture (hangman's fracture) can sever the spinal cord"},

    {"n":"Cervical vertebrae (C3-C7)","reg":"Spine","cnt":"5","tp":"Irregular",
     "fn":"Support and mobilise the neck; protect the cervical spinal cord; smallest vertebrae",
     "ff":"C7 has the longest spinous process — the prominent bump at the base of the neck; whiplash most commonly injures C4-C6"},

    {"n":"Thoracic vertebrae (T1-T12)","reg":"Spine","cnt":"12","tp":"Irregular",
     "fn":"Attach to the 12 pairs of ribs; protect the thoracic spinal cord; limited flexion/extension",
     "ff":"The most stable spinal region due to rib cage support; kyphosis (hunchback) typically occurs here"},

    {"n":"Lumbar vertebrae (L1-L5)","reg":"Spine","cnt":"5","tp":"Irregular",
     "fn":"Bear most of the body's axial load; allow trunk flexion and extension; no rib attachment",
     "ff":"Largest vertebrae in the spine; lumbar disc herniation is the most common cause of lower back pain and sciatica"},

    {"n":"Sacrum","reg":"Spine","cnt":"1 (5 fused)","tp":"Irregular",
     "fn":"Wedge-shaped; transfers weight from spine to pelvis; anchors pelvic girdle",
     "ff":"Formed by fusion of 5 vertebrae; the sacral hiatus is used for caudal epidural anaesthesia"},

    {"n":"Coccyx","reg":"Spine","cnt":"1 (3-5 fused)","tp":"Irregular",
     "fn":"Vestigial tail; provides attachment for pelvic floor muscles and ligaments",
     "ff":"A remnant of the tail found in our evolutionary ancestors; can be fractured in a fall onto hard surfaces"},

    # ── Thorax ────────────────────────────────────────────────────────────────
    {"n":"Sternum","reg":"Thorax","cnt":"1","tp":"Flat",
     "fn":"Protects heart and major vessels; anchors ribs via costal cartilage; landmark for CPR",
     "ff":"The xiphoid process (lower tip) is a CPR landmark; the sternum is the preferred site for bone marrow biopsy"},

    {"n":"True ribs (R1-R7)","reg":"Thorax","cnt":"14","tp":"Flat",
     "fn":"Protect lungs and heart; attach directly to sternum via costal cartilage; assist breathing",
     "ff":"The first rib is the shortest and most curved; rib fractures cause pain with every breath — pleurisy-like"},

    {"n":"False ribs (R8-R10)","reg":"Thorax","cnt":"6","tp":"Flat",
     "fn":"Protect lower lungs and upper abdominal organs; attach to rib 7 cartilage, not sternum",
     "ff":"Named 'false' because they do not reach the sternum directly; the costal margin formed by R8-R10 is a clinical landmark"},

    {"n":"Floating ribs (R11-R12)","reg":"Thorax","cnt":"4","tp":"Flat",
     "fn":"Protect kidneys; no anterior attachment; allow trunk rotation",
     "ff":"Only ribs with no anterior attachment; the 12th rib can be very short (3 cm); occasionally surgically removed for extra kidney access"},

    # ── Membre supérieur ──────────────────────────────────────────────────────
    {"n":"Clavicle","reg":"Shoulder","cnt":"2","tp":"Long",
     "fn":"Strut between sternum and shoulder blade; transmits forces from arm to axial skeleton",
     "ff":"The most frequently fractured bone — accounting for ~5 % of all fractures; the only horizontal long bone in the body"},

    {"n":"Scapula","reg":"Shoulder","cnt":"2","tp":"Flat",
     "fn":"Shoulder blade; glenoid cavity forms shoulder joint; 17 muscles attach to it",
     "ff":"The scapula 'floats' on the back — only the clavicle connects it to the skeleton; winged scapula occurs when serratus anterior is paralysed"},

    {"n":"Humerus","reg":"Upper arm","cnt":"2","tp":"Long",
     "fn":"Upper arm bone; proximal end forms shoulder joint; distal end forms elbow; attachment for rotator cuff",
     "ff":"The radial nerve winds around the humerus shaft — 'humeral shaft fracture' can paralyse wrist extension ('wrist drop')"},

    {"n":"Radius","reg":"Forearm","cnt":"2","tp":"Long",
     "fn":"Lateral (thumb side) forearm; rotates for supination/pronation; forms wrist joint with carpals",
     "ff":"Distal radius fracture (Colles fracture) is the most common wrist fracture — typical result of falling on an outstretched hand"},

    {"n":"Ulna","reg":"Forearm","cnt":"2","tp":"Long",
     "fn":"Medial forearm; olecranon forms point of elbow; forms stable hinge joint with humerus",
     "ff":"The olecranon is the bony point of the elbow — 'hitting your funny bone' is actually the ulnar nerve at the medial epicondyle of the humerus"},

    # ── Carpes ────────────────────────────────────────────────────────────────
    {"n":"Scaphoid","reg":"Wrist","cnt":"2","tp":"Short",
     "fn":"Proximal row; bridges proximal and distal carpal rows; transmits forces from hand to forearm",
     "ff":"The most commonly fractured carpal (70 % of carpal fractures); poor blood supply causes avascular necrosis if untreated"},

    {"n":"Lunate","reg":"Wrist","cnt":"2","tp":"Short",
     "fn":"Proximal row; central articulation with radius; key to wrist stability",
     "ff":"The most commonly dislocated carpal; lunate dislocation can compress the median nerve causing acute carpal tunnel syndrome"},

    {"n":"Triquetrum","reg":"Wrist","cnt":"2","tp":"Short",
     "fn":"Proximal row; articulates with pisiform and hamate; contributes to ulnar deviation",
     "ff":"Pyramid-shaped; 2nd most commonly fractured carpal; triquetral avulsion fracture is classic chip seen on lateral wrist X-ray"},

    {"n":"Pisiform","reg":"Wrist","cnt":"2","tp":"Sesamoid",
     "fn":"Sits in the flexor carpi ulnaris tendon; acts as a pulley to increase tendon leverage",
     "ff":"Only carpal classified as a sesamoid bone; pea-sized; Guyon's canal runs adjacent — ulnar nerve compression point"},

    {"n":"Trapezium","reg":"Wrist","cnt":"2","tp":"Short",
     "fn":"Distal row; forms the saddle joint with the 1st metacarpal — allows thumb opposition",
     "ff":"The thumb's saddle joint (trapeziometacarpal) is what enables human precision grip; osteoarthritis here is the most common hand arthritis"},

    {"n":"Trapezoid","reg":"Wrist","cnt":"2","tp":"Short",
     "fn":"Distal row; tightly wedged between trapezium and capitate; articulates with 2nd metacarpal",
     "ff":"Smallest distal carpal; the rarest carpal to fracture due to deep protective position — isolated fracture is extremely unusual"},

    {"n":"Capitate","reg":"Wrist","cnt":"2","tp":"Short",
     "fn":"Largest carpal; distal row centre; head articulates with lunate; keystone of wrist architecture",
     "ff":"Largest carpal bone; the 'keystone' of the carpus — its head is the most prominent structure felt in a wrist X-ray"},

    {"n":"Hamate","reg":"Wrist","cnt":"2","tp":"Short",
     "fn":"Distal row; hook (hamulus) forms wall of carpal tunnel; articulates with 4th and 5th metacarpals",
     "ff":"The hamulus hook can fracture from golf, tennis or baseball swings — a common missed diagnosis on plain X-ray"},

    {"n":"Metacarpal bones","reg":"Hand","cnt":"10","tp":"Long",
     "fn":"Form the palm; numbered 1 (thumb) to 5 (little finger); base of hand movements",
     "ff":"5th metacarpal neck fracture (Boxer's fracture) is the most common; 2nd metacarpal is longest and most rigid"},

    {"n":"Phalanges of hand","reg":"Hand","cnt":"28","tp":"Long",
     "fn":"Finger bones; 3 per finger (proximal, middle, distal) and 2 per thumb; grip and fine motor function",
     "ff":"14 per hand; distal phalanges house fingernails; fingertip amputation affects more people than any other traumatic amputation"},

    # ── Bassin ────────────────────────────────────────────────────────────────
    {"n":"Ilium","reg":"Pelvis","cnt":"2","tp":"Irregular",
     "fn":"Largest part of hip bone; forms the iliac crest; transfers spine load to acetabulum",
     "ff":"The iliac crest is the most common autograft donor site for bone grafting; the 'hip' we feel is actually the iliac crest"},

    {"n":"Ischium","reg":"Pelvis","cnt":"2","tp":"Irregular",
     "fn":"Posterior-inferior hip bone; ischial tuberosities bear sitting pressure; attachment for hamstrings",
     "ff":"The ischial tuberosities ('sit bones') support body weight when seated; ischial bursitis (tailor's bottom) is a repetitive-strain condition"},

    {"n":"Pubis","reg":"Pelvis","cnt":"2","tp":"Irregular",
     "fn":"Anterior hip bone; pubic symphysis joins left and right sides; forms obturator foramen with ischium",
     "ff":"Pubic symphysis separates up to 10 mm during childbirth; stress fractures common in runners and footballers ('osteitis pubis')"},

    # ── Membre inférieur ──────────────────────────────────────────────────────
    {"n":"Femur","reg":"Upper leg","cnt":"2","tp":"Long",
     "fn":"Transfers weight from hip to knee; attachment for the most powerful muscles in the body",
     "ff":"Longest and strongest bone in the human body; femoral neck fracture in the elderly is a life-threatening orthopaedic emergency"},

    {"n":"Patella","reg":"Knee","cnt":"2","tp":"Sesamoid",
     "fn":"Protects the knee joint; increases the leverage (mechanical advantage) of the quadriceps by ~50 %",
     "ff":"Largest sesamoid bone; develops within the quadriceps tendon; bipartite patella (naturally in two pieces) occurs in ~2 % of people"},

    {"n":"Tibia","reg":"Lower leg","cnt":"2","tp":"Long",
     "fn":"Shinbone; bears ~80 % of body weight; medial malleolus forms inner ankle; tibial tuberosity anchors patellar tendon",
     "ff":"2nd strongest bone; tibial shaft stress fracture is the most common running injury; the flat anteromedial surface has no muscle covering"},

    {"n":"Fibula","reg":"Lower leg","cnt":"2","tp":"Long",
     "fn":"Lateral leg; lateral malleolus forms outer ankle; not weight-bearing; muscle attachment",
     "ff":"Bears < 10 % of body weight but the lateral malleolus is the most commonly fractured ankle bone; fibula graft used in mandible reconstruction"},

    # ── Tarse ────────────────────────────────────────────────────────────────
    {"n":"Calcaneus","reg":"Foot","cnt":"2","tp":"Short",
     "fn":"Heel bone; largest tarsal; Achilles tendon attaches posteriorly; forms subtalar joint",
     "ff":"Largest bone in the foot; calcaneal fractures (falling from height) are the most common tarsal fractures — causes severe chronic pain"},

    {"n":"Talus","reg":"Foot","cnt":"2","tp":"Short",
     "fn":"Ankle bone; transmits entire body weight from tibia to foot; links ankle to subtalar and midtarsal joints",
     "ff":"The only bone in the foot with no muscle attachments; covered 60 % by cartilage; avascular necrosis risk after fracture"},

    {"n":"Navicular","reg":"Foot","cnt":"2","tp":"Short",
     "fn":"Boat-shaped medial tarsal; keystone of the medial longitudinal arch; articulates with talus and cuneiforms",
     "ff":"Navicular stress fracture is the most serious in sport — occurs in sprinters and basketball players; slow to heal due to poor blood supply"},

    {"n":"Cuboid","reg":"Foot","cnt":"2","tp":"Short",
     "fn":"Lateral tarsal; forms peroneal groove (peroneus longus route); articulates with calcaneus and 4th-5th metatarsals",
     "ff":"Cuboid syndrome (subluxation) causes lateral foot pain in dancers and athletes; the peroneal groove makes it unique among tarsals"},

    {"n":"Medial cuneiform","reg":"Foot","cnt":"2","tp":"Short",
     "fn":"Largest cuneiform; medial foot; articulates with navicular, intermediate cuneiform, and 1st metatarsal",
     "ff":"Forms the medial column of the Lisfranc joint; Lisfranc injuries (ligament tears here) are often missed on initial X-ray"},

    {"n":"Intermediate cuneiform","reg":"Foot","cnt":"2","tp":"Short",
     "fn":"Middle cuneiform; articulates with navicular, adjacent cuneiforms, and 2nd metatarsal",
     "ff":"Smallest and most wedge-shaped cuneiform; its recessed position locks the 2nd metatarsal — this is why 2nd MTP is stable but the joint injures in Lisfranc trauma"},

    {"n":"Lateral cuneiform","reg":"Foot","cnt":"2","tp":"Short",
     "fn":"Lateral wedge bone; articulates with navicular, cuboid, intermediate cuneiform, and 3rd metatarsal",
     "ff":"Completes the transverse arch of the foot alongside the cuboid; cuneiform fractures are rare in isolation"},

    {"n":"Metatarsal bones","reg":"Foot","cnt":"10","tp":"Long",
     "fn":"Connect tarsals to toes; form the forefoot arch; transmit propulsive forces during walking and running",
     "ff":"The 2nd metatarsal is longest and bears the most stress ('march fracture' in soldiers and runners); 5th metatarsal base avulsion is the most common foot fracture"},

    {"n":"Phalanges of foot","reg":"Foot","cnt":"28","tp":"Long",
     "fn":"Toe bones; propulsion and balance; 3 per toe except hallux (big toe) which has 2",
     "ff":"The hallux (big toe) bears 40-60 % of forward propulsion; hallux valgus (bunion) deformity of the 1st MTP affects ~23 % of adults"},
]
