function Construct_jplex_cpx(InFolder, OutFolder)

    javaaddpath('../../../../softwares/javaplex/lib/javaplex.jar');
    import edu.stanford.math.plex4.*;

    javaaddpath('../../../../softwares/javaplex/lib/plex-viewer.jar');
    import edu.stanford.math.plex_viewer.*;

    addpath('../../../../softwares/javaplex/utility');
    
    formatSpec = '%d %f %f %f';
    sizeA = [4,Inf];
    
    Elements = {'C','N','O'};
    
    for j=1:3
        for k=1:3
            e1 = Elements{j}; e2 = Elements{k};
            WildName = strcat('wild_mutation_',e1,'_',e2,'.pts');
            WildOutName = strcat('wild_mutation_',e1,'_',e2,'.PH');
            fileID = fopen(strcat('./', WildName), 'r');
            A = fscanf(fileID, formatSpec, sizeA);
            fclose(fileID);
            distances = ones(size(A,2),size(A,2)).*100.0;
            for ii=1:size(A,2)
                for jj=(ii+1):size(A,2)
                    if A(1,ii)+A(1,jj) == 1
                        dis = sqrt((A(2,ii) - A(2,jj))^2 + (A(3,ii) - A(3,jj))^2 + (A(4,ii) - A(4,jj))^2);
                        distances(ii,jj) = dis;
                        distances(jj,ii) = dis;
                        distances(ii,ii) = 0.0;
                    end
                end
            end
            m_space = metric.impl.ExplicitMetricSpace(distances);
            stream = api.Plex4.createVietorisRipsStream(m_space, 1, 15.0, 200);
            persistence = api.Plex4.getModularSimplicialAlgorithm(1, 2);
            intervals = persistence.computeIntervals(stream);
            endpoints = homology.barcodes.BarcodeUtility.getEndpoints(intervals, 0, false);
            dims = zeros(1,size(endpoints,1));
            bars = [dims; endpoints(:,1)'; endpoints(:,2)'];
            fileID = fopen (strcat('./', WildOutName), 'w');
            fprintf(fileID, '%d %4.4f %4.4f\n', bars);
   
            fclose(fileID);
        end
    end
    
    for j=1:3
        for k=1:3
            e1 = Elements{j}; e2 = Elements{k};
            MutName = strcat('mut_mutation_',e1,'_',e2,'.pts');
            MutOutName = strcat('mut_mutation_',e1,'_',e2,'.PH');
            fileID = fopen(strcat('./', MutName), 'r');
            A = fscanf(fileID, formatSpec, sizeA);
            fclose(fileID);
            distances = ones(size(A,2),size(A,2)).*100.0;
            for ii=1:size(A,2)
                for jj=(ii+1):size(A,2)
                    if A(1,ii)+A(1,jj) == 1
                        dis = sqrt((A(2,ii) - A(2,jj))^2 + (A(3,ii) - A(3,jj))^2 + (A(4,ii) - A(4,jj))^2);
                        distances(ii,jj) = dis;
                        distances(jj,ii) = dis;
                        distances(ii,ii) = 0.0;
                    end
                end
            end
            m_space = metric.impl.ExplicitMetricSpace(distances);
            stream = api.Plex4.createVietorisRipsStream(m_space, 1, 15.0, 200);
            persistence = api.Plex4.getModularSimplicialAlgorithm(1, 2);
            intervals = persistence.computeIntervals(stream);
            endpoints = homology.barcodes.BarcodeUtility.getEndpoints(intervals, 0, false);
            dims = zeros(1,size(endpoints,1));
            bars = [dims; endpoints(:,1)'; endpoints(:,2)'];
            fileID = fopen (strcat('./', MutOutName), 'w');
            fprintf(fileID, '%d %4.4f %4.4f\n', bars);
            fclose(fileID);
        end
    end
exit
