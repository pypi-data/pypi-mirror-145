import sys

def i(*vargs):
	log("[INFO]:", *vargs)

def w(*vargs):
	log("[WARN]:", *vargs)

def d(*vargs):
	log("[DEBUG]:", *vargs)

def e(*vargs):
	log("[ERROR]:", *vargs)

def f(*vargs):
	log("[FATAL]:", *vargs)

def log(tag, *vargs):
	write(tag)
	write(' '.join(map(str, [*vargs])))
	write('\n')

def write(sz):
	sys.stderr.write(sz)