```
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
cd android
./gradlew assembleRelease
```

# build front and mobile from repository root

```
cd frontrend
npm run build
cd mobile
npx cap sync
cd android
./gradlew assembleRelease
```

# start emulator
```
emulator -list-avds
emulator -avd Pixel_2_API_31
```

# install to emulator, run from mobile folder

```
adb install -r android/app/build/outputs/apk/release/app-release.apk
```

# frontend update workflow

```
cd ..
npx cap sync
cd android/
./gradlew assembleRelease
adb install -r app/build/outputs/apk/release/app-release.apk

```