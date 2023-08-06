#! /bin/bash

echo "-------- Building Indago --------"
echo " Please choose target: [TestPyPI]/PyPI:"
read target

if [ -z "$target" ];
then
target="TestPyPI"
fi

if [[ $target != "TestPyPI" ]] && [[ $target != "PyPI" ]];
then
echo "Unsupported target: " $target
exit
fi
echo "Using target " $target


rm -r build dist Indago.egg-info 
/opt/anaconda3/bin/python setup.py clean sdist bdist_wheel 

if [[ $target == "TestPyPI" ]];
then
/opt/anaconda3/bin/python3 -m twine upload --repository testpypi dist/*
/opt/anaconda3/bin/python3 -m pip install --upgrade --force-reinstall --index-url https://test.pypi.org/simple/ indago
fi

if [[ $target == "PyPI" ]];
then
/opt/anaconda3/bin/python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
fi
