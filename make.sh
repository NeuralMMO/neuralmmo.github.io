rm -r source/autodoc/*
make clean

#Don't use: 
#  undoc-members (pollutes with garbage internals)
#  imported-members (pollutes with inhereted garbage)

SPHINX_APIDOC_OPTIONS=members,undoc-members,inherited-members,show-inheritance sphinx-apidoc -o source/autodoc/ -fMe --implicit-namespaces ../environment/nmmo/

#Strip bad headers
for f in source/autodoc/*.rst; do\
   python postprocess.py $f
done

make html